import argparse
import socket
import json
import logging 

# Set up the logger
logging.basicConfig(filename="air_traffic.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


# Store passenger as a dictionary
def route_passenger(mapping, fname, lname, origin, destination, layover=None):
    passenger = {
        'fname': fname,
        'lname': lname,
        'origin': origin,
        'destination': destination,
        'layover': layover
    }

    port = mapping['hubs'].get(origin) or mapping['spokes'].get(origin)
    if port:
        # Create a UDP socket as the client
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(json.dumps(passenger).encode('utf-8'), ('localhost', port))
        # Close the socket
        s.close()

if __name__ == "__main__":
    # This is only here to write a space in the log between each of the passengers
    new_empty_line = open('air_traffic.log','a+')
    new_empty_line.write('\n')
    new_empty_line.close()

    # Classification of airports as hubs and spokes
    mapping = {
        'hubs': {
            'ANC': 8080,
            'FAI': 8081,
            'SEA': 8082
        },
        'spokes': {
            'BRW': 8083,
            'OTZ': 8084,
            'SCC': 8085,
            'BET': 8086,
            'JNU': 8087
        }
    }

    parser = argparse.ArgumentParser(description="Route a passenger")
    parser.add_argument("fname", help="Passenger's first name")
    parser.add_argument("lname", help="Passenger's last name")
    parser.add_argument("origin", help="Origin airport code")
    parser.add_argument("destination", help="Destination airport code")
    parser.add_argument("--layover", default=None, help="Layover airport, if any")
    args = parser.parse_args()

    # Log user input
    if args.layover == None:
        logger.info(f"You typed: python route_passenger.py {args.fname} {args.lname} {args.origin} {args.destination}")
    else:
        logger.info(f"You typed: python route_passenger.py {args.fname} {args.lname} {args.origin} {args.destination} --layover {args.layover}")



    # A whole lot of input checking
    # Origin and destination may not be the same
    if args.origin == args.destination:
        print('Origin may not be the same as destination.')
        logger.warning('Origin may not be the same as destination.')

    # Layover may not be the same as origin or destination
    elif args.layover and (args.origin == args.layover) or (args.destination == args.layover):
        print('Layover may not be the same as origin or destination.')
        logger.warning('Layover may not be the same as origin or destination.')

    # If there is a layover, it must be at a hub and that hub must exist
    elif args.layover and args.layover not in mapping['hubs']:
        print('Invalid layover airport. Layover airport must be a hub: ANC, FAI, or SEA')
        logger.warning('Invalid layover airport. Layover airport must be a hub: ANC, FAI, or SEA')

    # Direct flights between small airports without a layover at a hub are not permitted
    elif (not args.layover and (args.origin in mapping['spokes'] and args.destination in mapping['spokes'])):
        print('Attempted direct flight between small airports. Direct flights between small airports are not offered.')
        logger.warning('Attempted direct flight between small airports. Direct flights between small airports are not offered.')

    # Making sure destination airport and origin airport exist in the list of airports
    elif not (args.origin in mapping['hubs'] or args.origin in mapping['spokes']):
        print('Origin airport code and destination airport code must be in the list of airport codes.')
        logger.warning('Origin airport code and destination airport code must be in the list of airport codes.')
    elif not (args.destination in mapping['hubs'] or args.destination in mapping['spokes']):
        print('Origin airport code and destination airport code must be in the list of airport codes.')
        logger.warning('Origin airport code and destination airport code must be in the list of airport codes.')

    # Otherwise if all is good, route the passenger
    else:
        print(f"Routing passenger {args.fname} {args.lname} from {args.origin} to {args.destination}.") 
        logger.info(f"Routing passenger {args.fname} {args.lname} from {args.origin} to {args.destination}.") 

        # If all is good, route the passenger
        route_passenger(mapping, args.fname, args.lname, args.origin, args.destination, args.layover)
