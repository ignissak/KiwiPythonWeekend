"""
Python Weekend Task 2021
(c) Jakub Bordáš
"""
import argparse
import csv
import json
from datetime import datetime

parser = argparse.ArgumentParser()

# Required arguments
parser.add_argument('data_file', type=str,
                    help='A required data file name')
parser.add_argument('origin_location', type=str,
                    help='A required origin location of trip')
parser.add_argument('destination_location', type=str,
                    help='A required destination location of trip')

# Optional arguments
parser.add_argument('--bags', type=int,
                    help='Number of requested bags [default=0]',
                    default=0)
parser.add_argument('--max_price', type=float,
                    help='Maximum price for trip (including required amount of bags)',
                    default=-1)
parser.add_argument('--max_bag_price', type=int,
                    help='Maximum price per bag',
                    default=-1)
parser.add_argument('--disable_transfer_flights', action='store_true',
                    help='Should disable transfer flights? [default=false]',
                    default=False)
parser.add_argument('--return_flight', action='store_true',
                    help='Should search for a return flight? [default=false]',
                    default=False)

args = parser.parse_args()

data_file = args.data_file
origin_location = args.origin_location
destination_location = args.destination_location
bags = args.bags
max_price = args.max_price
max_bag_price = args.max_bag_price
disable_transfer_flights = args.disable_transfer_flights
return_flight = args.return_flight

flights_data = []

try:
    with open(data_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            flights_data.append(row)
except FileNotFoundError:
    parser.error(f'File was not found ({data_file}.')


def find_direct_flights(origin, destination):
    """
    Finds direct flights from origin to destination.
    :param origin: Origin airport code
    :param destination: Destination airport code
    :return: List of usable direct flights. This list may be empty if no direct flights are found.
    """
    return list(filter(lambda flight: flight['origin'] == origin and flight['destination'] == destination,
                       flights_data))


def parse_flight_time(flight, time_type):
    """
    Parses flight's arrival/departure time
    :param flight:
    :param time_type: Type of time (only arrival/departure)
    :return: Parsed datetime
    """
    if time_type != 'arrival' and time_type != 'departure':
        raise Exception("Invalid parameter " + time_type)
    if type(flight) is list:
        return datetime.strptime(flight[0][time_type].replace("T", " "),
                                 "%Y-%m-%d %H:%M:%S")
    else:
        return datetime.strptime(flight[time_type].replace("T", " "),
                                 "%Y-%m-%d %H:%M:%S")


def can_connect(f1, f2):
    """
    Checks if two flights follow layover restrictions and can be used as connecting flights.
    :param f1: First flight
    :param f2: Second flight
    :return: True if flights can connect, otherwise false
    """
    f1_time = parse_flight_time(f1, 'arrival')
    f2_time = parse_flight_time(f2, 'departure')

    if f1_time > f2_time:
        return False

    diff = f2_time - f1_time
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    #print(hours)
    if 6 > hours > 1:
        return True
    return False


def is_flight_after_other(f1, f2):
    """
    Checks if second flight's departure time is past first flight's arrival time. This is used to determine if certain
    flight can be used as returning flight to origin destination. Layover restrictions do not apply here.
    :param f1: First flight
    :param f2: Second flight
    :return: True if second flight's departure time is past first flight's arrival time, otherwise false.
    """
    f1_time = parse_flight_time(f1, 'arrival')
    f2_time = parse_flight_time(f2, 'departure')

    if f2_time > f1_time:
        return True
    return False


def find_connection_flights(origin, destination):
    """
    Checks for connection flights from origin airport to destination airport.
    :param origin: Origin airport code
    :param destination: Desination airport code
    :return: List of two flights if this trip is possible, otherwise returns an empty list
    """
    possible = []
    for f1 in filter(lambda flight: flight['origin'] == origin, flights_data):
        # Origin is the same
        destination1 = f1['destination']
        for f2 in filter(lambda flight: flight['origin'] == destination1 and flight['destination'] == destination,
                         flights_data):
            if can_connect(f1, f2):
                #print(json.dumps([f1, f2], indent=4))
                # These flights can be connected
                possible.append([f1, f2])
    return possible


def print_final(combos):
    """
    Prints final JSON result of trips
    :param combos: List of flights
    """
    final = []
    if return_flight:
        # We are also parsing returning flights
        for combo in combos:
            # print(json.dumps(combo, indent=4))
            bags_allowed = None
            bag_price = None
            flight_price = None
            total_price = None
            travel_time = None
            if type(combo[0]) is list:
                bags_allowed = min(int(f['bags_allowed']) for f in combo[0])
                if bags > bags_allowed:
                    # Not enough baggage
                    continue
                bag_price = sum(int(f['bag_price']) * bags for f in combo[0])
                if bag_price > max_bag_price != -1:
                    # Too expensive bag price
                    continue
                flight_price = sum(float(f['base_price']) for f in combo[0])
                total_price = flight_price + bag_price
                if total_price > max_price != -1:
                    # Too expensive
                    continue
                travel_time = parse_flight_time(combo[0][-1], 'arrival') - parse_flight_time(combo[0][0], 'departure')
            else:
                bags_allowed = min(int(f['bags_allowed']) for f in combo)
                if bags > bags_allowed:
                    # Not enough baggage
                    continue
                bag_price = sum(int(f['bag_price']) * bags for f in combo)
                if bag_price > max_bag_price != -1:
                    # Too expensive bag price
                    continue
                flight_price = sum(float(f['base_price']) for f in combo)
                total_price = flight_price + bag_price
                if total_price > max_price != -1:
                    # Too expensive
                    continue
                travel_time = parse_flight_time(combo[-1], 'arrival') - parse_flight_time(combo[0], 'departure')
            d = {
                "flights": combo,
                "bags_allowed": bags_allowed,
                "bags_count": bags,
                "destination": destination_location,
                "origin": origin_location,
                "flight_price": flight_price,
                "bag_price": bag_price,
                "total_price": total_price,
                "travel_time": str(travel_time)
            }
            final.append(d)
    else:
        # No returning flights
        for flight in combos:
            # print(json.dumps(flight, indent=4))
            if type(flight) is list:
                # print('JE LIST')
                # Connecting flights
                bags_allowed = min(int(f['bags_allowed']) for f in flight)
                if bags > bags_allowed:
                    # Not enough baggage
                    continue
                bag_price = sum(int(f['bag_price']) * bags for f in flight)
                if bag_price > max_bag_price != -1:
                    # Too expensive bag price
                    continue
                flight_price = sum(float(f['base_price']) for f in flight)
                total_price = flight_price + bag_price
                if total_price > max_price != -1:
                    # Too expensive
                    continue
                travel_time = parse_flight_time(flight[-1], 'arrival') - parse_flight_time(flight[0], 'departure')
                d = {
                    "flights": flight,
                    "bags_allowed": bags_allowed,
                    "bags_count": bags,
                    "destination": destination_location,
                    "origin": origin_location,
                    "flight_price": flight_price,
                    "bag_price": bag_price,
                    "total_price": total_price,
                    "travel_time": str(travel_time)
                }
                final.append(d)
            else:
                bags_allowed = int(flight['bags_allowed'])
                if bags > bags_allowed:
                    # Not enough baggage
                    continue
                bag_price = int(flight['bag_price'])
                if bag_price > max_bag_price != -1:
                    # Too expensive bag price
                    continue
                flight_price = float(flight['base_price'])
                total_price = flight_price + bag_price
                if total_price > max_price != -1:
                    # Too expensive
                    continue
                travel_time = parse_flight_time(flight, 'arrival') - parse_flight_time(flight, 'departure')
                d = {
                    "flights": flight,
                    "bags_allowed": bags_allowed,
                    "bags_count": bags,
                    "destination": destination_location,
                    "origin": origin_location,
                    "flight_price": flight_price,
                    "bag_price": bag_price,
                    "total_price": total_price,
                    "travel_time": str(travel_time)
                }
                final.append(d)

    final = sorted(final, key=lambda trip: trip['total_price'])
    print(json.dumps(final, indent=4))
    print(len(final))


# Find direct and connecting flights from origin to destination
direct_flights = find_direct_flights(origin_location, destination_location)
connecting_flights = find_connection_flights(origin_location, destination_location)

if return_flight:
    # Find returning flight(s)
    returning_direct_flights = find_direct_flights(destination_location, origin_location)
    returning_connecting_flights = find_connection_flights(destination_location, origin_location)
    possible_combos = []
    for direct_flight in direct_flights:
        for returning_direct_flight in returning_direct_flights:
            if is_flight_after_other(direct_flight, returning_direct_flight):
                possible_combos.append([direct_flight, returning_direct_flight])

    # Check if connecting flights can connect
    # print(json.dumps(connecting_flights + returning_connecting_flights, indent=4))
    if not disable_transfer_flights:
        for connecting_flight in connecting_flights:
            for returning_connecting_flight in returning_connecting_flights:
                if is_flight_after_other(connecting_flight, returning_connecting_flight):
                    possible_combos.append([connecting_flight, returning_connecting_flight])
    print_final(possible_combos)
else:
    # print(json.dumps(connecting_flights, indent=4))
    # print(json.dumps(direct_flights, indent=4))
    x = []
    x.extend(direct_flights)
    if not disable_transfer_flights:
        x.extend(connecting_flights)
    print_final(x)
