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


locationsRequest = requests.get('https://brn-ybus-pubapi.sa.cz/restapi/consts/locations')
locationData = json.loads(locationsRequest.content)

# PARSER
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
dateString = date.strftime('%Y-%m-%d')

originId = None
destinationId = None


def find_city_id(name, data):
    for country in data:
        for city in country['cities']:
            if city['name'] == name or name in city['aliases']:
                return city['id']


request = requests.get('https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple',
                       params={
                           'departureDate': dateString,
                           'fromLocationId': originId,
                           'toLocationId': destinationId,
                           'fromLocationType': 'CITY',
                           'toLocationType': 'CITY',
                           'tariffs': 'REGULAR'
                       })

routes = json.loads(request.content)
output = []

for route in routes['routes']:
    output.append({
        'route_id': route['id'],
        'type': route['vehicleTypes'][0],
        'departure_id': route['departureStationId'],
        'destination_id': route['arrivalStationId'],
        'departure': origin,
        'destination': destination,
        'departure_time': route['departureTime'],
        'arrival_time': route['arrivalTime'],
        'price_from': route['priceFrom'],
        'price_to': route['priceTo'],
        'free_seats': route['freeSeatsCount'],
        'travel_time': ' '.join(route['travelTime'].split()),
        'bookable': route['bookable'],
        'delay': route['delay']
    })

print(json.dumps(output, indent=4))
