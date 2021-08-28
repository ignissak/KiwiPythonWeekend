import argparse
import datetime
import json

import requests


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


class RegioJet:

    def __init__(self):
        self.LOCATIONS_URL = 'https://brn-ybus-pubapi.sa.cz/restapi/consts/locations'
        self.SEARCH_URL = 'https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple'

        self.locations = None

    def find_city_id_by_name(self, name, data):
        """
        Finds city ID by its name in entered data object.
        :param name: Name of the city
        :param data: Data object (json)
        :return: ID of the city
        """
        for country in data:
            for city in country['cities']:
                if city['name'] == name or name in city['aliases']:
                    return city['id']

    def find_city_name_by_id(self, city_id, data):
        """
        Find city name by its ID in intered data object,
        :param city_id: ID of the city
        :param data: Data object (json)
        :return: Name of the city
        """
        for country in data:
            for city in country['cities']:
                if city['id'] == city_id:
                    return city['name']

    def find_locations(self):
        """
        Finds IDs of all available locations.
        :return: JSON object of all available countries and cities and their IDs.
        """
        if self.locations is None:
            locationsRequest = requests.get(self.LOCATIONS_URL)
            self.locations = json.loads(locationsRequest.content)
        return self.locations

    def find_routes(self, date, origin_id, destination_id):
        """
        Finds all routes after certain date from origin to destination.
        :param date: Date in format %Y-%M-%d
        :param origin_id: ID of the origin city
        :param destination_id: ID of the destination city
        :return: JSON object of all available routes
        """
        request = requests.get(self.SEARCH_URL,
                               params={
                                   'departureDate': date,
                                   'fromLocationId': origin_id,
                                   'toLocationId': destination_id,
                                   'fromLocationType': 'CITY',
                                   'toLocationType': 'CITY',
                                   'tariffs': 'REGULAR'
                               })

        return json.loads(request.content)['routes']

    def format_route(self, route):
        return {
            'route_id': route['id'],
            'type': route['vehicleTypes'][0],
            'departure_id': route['departureStationId'],
            'destination_id': route['arrivalStationId'],
            'departure': self.find_city_name_by_id(route['departureStationId'], self.find_locations()),
            'destination': self.find_city_name_by_id(route['arrivalStationId'], self.find_locations()),
            'departure_time': route['departureTime'],
            'arrival_time': route['arrivalTime'],
            'price_from': route['priceFrom'],
            'price_to': route['priceTo'],
            'free_seats': route['freeSeatsCount'],
            'travel_time': ' '.join(route['travelTime'].split()),
            'bookable': route['bookable'],
            'delay': route['delay']
        }

    def format_routes(self, routes):
        return [self.format_route(route) for route in routes]


regioJet = RegioJet()

# CLI Argument parsing logic
parser = argparse.ArgumentParser()

parser.add_argument('origin', type=str,
                    help='Origin location')
parser.add_argument('destination', type=str,
                    help='Destination location')
parser.add_argument('date', type=valid_date,
                    help='Start date - format YYYY-MM-DD')

arguments = parser.parse_args()

origin = arguments.origin
destination = arguments.destination
date = arguments.date
date_string = date.strftime('%Y-%m-%d')

locations = regioJet.find_locations()
originId = regioJet.find_city_id_by_name(origin, locations)
destinationId = regioJet.find_city_id_by_name(destination, locations)
routes = regioJet.find_routes(date_string, originId, destinationId)

print(json.dumps(regioJet.format_routes(routes), indent=4))