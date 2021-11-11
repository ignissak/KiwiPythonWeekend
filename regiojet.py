import argparse
import datetime
import json
import time

import pytz as pytz
import redis as s
import requests
from slugify import slugify

import config
from db import Database, Journey


def current_milli_time():
    return round(time.time() * 1000)


def valid_date(date_string):
    try:
        return datetime.datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date_string)
        raise argparse.ArgumentTypeError(msg)


class RegioJet:
    database = Database()

    def __init__(self):
        self.LOCATIONS_URL = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/locations'
        self.SEARCH_URL = 'https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple'

        redis_config = {'host': config.REDIS_URL, 'port': 6379,
                        'decode_responses': True, 'charset': 'utf-8'}
        self.redis = s.Redis(**redis_config)

    def find_city_id_by_name(self, name, data):
        """
        Finds location (station/city) ID by its name in entered data object.
        :param name: Name of the city
        :param data: Data object (json)
        :return: ID of the location
        """
        if self.redis.exists(f'bordas:location_id:{slugify(name, separator="_")}'):
            return self.redis.get(f'bordas:location_id:{slugify(name, separator="_")}')
        for country in data:
            for city in country['cities']:
                if city['name'] == name or name in city['aliases']:
                    cityId = city['id']
                    self.redis.set(f'bordas:location_id:{slugify(name, separator="_")}', cityId, ex=60)
                    return cityId
                for station in city['stations']:
                    if station['name'] == name or station['fullname'] == name:
                        stationId = station['id']
                        self.redis.set(f'bordas:location_id:{slugify(name, separator="_")}', stationId, ex=60)
                        return

    def find_location_name_by_id(self, location_id, data):
        """
        Find location (station/city) name by its ID in intered data object,
        :param location_id: ID of the city
        :param data: Data object (json)
        :return: Name of the location
        """
        if self.redis.exists(f'bordas:location_name:{location_id}'):
            return self.redis.get(f'bordas:location_name:{location_id}')
        for country in data:
            for city in country['cities']:
                if city['id'] == location_id:
                    city = city['name']
                    self.redis.set(f'bordas:location_name:{location_id}', city, ex=60)
                    return city
                for station in city['stations']:
                    if station['id'] == location_id:
                        station = station['fullname']
                        self.redis.set(f'bordas:location_name:{location_id}', station, ex=60)
                        return station

    def find_locations(self):
        """
        Finds IDs of all available locations.
        :return: JSON object of all available countries and cities and their IDs.
        """
        if not self.redis.exists('bordas:locations'):
            locationsRequest = requests.get(self.LOCATIONS_URL)
            self.redis.set("bordas:locations", locationsRequest.content, ex=120)
            return json.loads(locationsRequest.content)
        return json.loads(self.redis.get("bordas:locations"))

    def find_routes(self, date_from, date_to, origin_id, destination_id, origin_name, destination_name, passengers=1):
        """
        Finds all routes after certain date from origin to destination.
        :param destination_name: Destination's name
        :param origin_name: Origin's name
        :param passengers: Minimum amount of passengers
        :param date_from: Date in format %Y-%M-%d
        :param date_to: Date in format %Y-%M-%d
        :param origin_id: ID of the origin city
        :param destination_id: ID of the destination city
        :return: JSON object of all available routes
        """
        # Check Redis
        if self.redis.exists(
                f'bordas:routes:{origin_name}_{destination_name}_{passengers}_{date_from}_{date_to}'):
            return json.loads(self.redis.get(
                f'bordas:routes:{origin_name}_{destination_name}_{passengers}_{date_from}_{date_to}'))

        # Check database
        databaseResult = self.database.find_journeys(origin_name, destination_name, self.format_custom_time(date_from),
                                                     self.format_custom_time(date_to))
        if len(databaseResult) > 0:
            # There is something in database
            formattedResult = [self.format_route(journey) for journey in databaseResult]
            self.redis.set(
                f'bordas:routes:{origin_name}_{destination_name}_{passengers}_{date_from}_{date_to}',
                json.dumps(formattedResult), ex=60)
            return formattedResult

        # Scrap
        request = requests.get(self.SEARCH_URL,
                               params={
                                   'departureDate': date_from,
                                   'fromLocationId': origin_id,
                                   'toLocationId': destination_id,
                                   'fromLocationType': 'CITY',
                                   'toLocationType': 'CITY',
                                   'tariffs': 'REGULAR'
                               })

        self.verify_route(request.content)

        result = json.loads(request.content)['routes']
        result[:] = [x for x in result if self.determine_dates(x['departureTime'], date_to)]

        # utc = pytz.timezone('Europe/Bratislava')
        # for route in result:
        #     print(datetime.datetime.fromisoformat(route['departureTime']))
        #     print(utc.localize(datetime.datetime.strptime(date_to, "%Y-%m-%d")))
        #     if datetime.datetime.fromisoformat(route['departureTime']) > utc.localize(
        #             datetime.datetime.strptime(date_to, "%Y-%m-%d")):
        #         result.remove(route)
        #     else:
        #         print(route['id'])

        # Checking for parameters

        result[:] = [x for x in result if x['freeSeatsCount'] >= passengers]

        for route in result:
            route['priceFrom'] *= passengers
            route['priceTo'] *= passengers

        # if passengers > 1:
        #     for (index, route) in enumerate(result):
        #         if route['freeSeatsCount'] >= passengers:
        #             route['priceFrom'] *= passengers
        #             route['priceTo'] *= passengers
        #             del result[index]

        for session in self.database.create_session():
            for route in result:
                journey = Journey(
                    origin=slugify(origin_name, separator="_"),
                    destination=slugify(destination_name, separator="_"),
                    departure_datetime=self.format_iso(route['departureTime']),
                    arrival_datetime=self.format_iso(route['arrivalTime']),
                    carrier='regiojet',
                    vehicle_type=slugify(route['vehicleTypes'][0], separator="_"),
                    price=route['priceFrom'],
                    currency='EUR')
                session.add(journey)
            session.commit()
            session.close()

        self.redis.set(
            f'bordas:routes:{origin_name}_{destination_name}_{passengers}_{date_from}_{date_to}',
            json.dumps(result), ex=60)
        return result

    def format_route(self, route):
        if type(route) is dict:
            formatted = {
                'type': route['type'],
                'departure': route['departure'],
                'destination': route['destination'],
                'departure_time': route['departure_time'],
                'arrival_time': route['arrival_time'],
                'price': route['price'],
                'carrier': slugify('REGIOJET'),
                'currency': slugify('EUR')
            }
            return formatted
        elif type(route) is Journey:
            formatted = {
                'type': route.vehicle_type,
                'departure': route.origin,
                'destination': route.destination,
                'departure_time': route.departure_datetime.isoformat(),
                'arrival_time': route.arrival_datetime.isoformat(),
                'price': route.price,
                'carrier': route.carrier,
                'currency': route.currency
            }
            return formatted

    def format_routes(self, routes):
        return [self.format_route(route) for route in routes]

    def verify_route(self, request_content):
        j = json.loads(request_content)
        if 'errorFields' in j:
            raise AttributeError(f'{j["message"]} ' + str(j['errorFields']))

    def determine_dates(self, date_from, date_to):
        utc = pytz.timezone('Europe/Bratislava')
        return not datetime.datetime.fromisoformat(date_from) > utc.localize(
            datetime.datetime.strptime(date_to, "%Y-%m-%d"))

    def format_custom_time(self, time):
        return datetime.datetime.strptime(time, "%Y-%m-%d")

    def format_iso(self, time):
        return datetime.datetime.fromisoformat(time)

    def get_all_cities_names(self):
        locs = self.find_locations()
        output = []
        for country in locs:
            for city in country['cities']:
                output.append(city['name'])
        return output

# regioJet = RegioJet()
#
# # CLI Argument parsing logic
# parser = argparse.ArgumentParser()
#
# parser.add_argument('origin', type=str,
#                     help='Origin location')
# parser.add_argument('destination', type=str,
#                     help='Destination location')
# parser.add_argument('date', type=valid_date,
#                     help='Start date - format YYYY-MM-DD')
# parser.add_argument('--clear_cache', action='store_true',
#                     default=False)
#
# arguments = parser.parse_args()
#
# origin = arguments.origin
# destination = arguments.destination
# date = arguments.date
# date_string = date.strftime('%Y-%m-%d')
# clear_cache = arguments.clear_cache
#
# if clear_cache:
#     for key in regioJet.redis.keys():
#         if key.startswith("bordas"):
#             regioJet.redis.delete(key)
#     exit()
#
# locations = regioJet.find_locations()
# originId = regioJet.find_city_id_by_name(origin, locations)
# destinationId = regioJet.find_city_id_by_name(destination, locations)
# routes = regioJet.find_routes(date_string, originId, destinationId)
#
# print(json.dumps(regioJet.format_routes(routes), indent=4))
