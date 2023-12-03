import socket
import json
import argparse
import logging
import signal

# Set up the logger
logging.basicConfig(filename="air_traffic.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Airport class
class Airport:
    def __init__(self, code):
        self.code = code
        self.mapping = {
        'ANC': 8080,
        'FAI': 8081,
        'SEA': 8082,
        'BRW': 8083,
        'OTZ': 8084,
        'SCC': 8085,
        'BET': 8086,
        'JNU': 8087
        }
        
        # Set up a flag to indicate whether the script should continue running
        self.running = True

        # Set up a signal handler for SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        # Handle the SIGINT signal (Ctrl+C)
        print(f"Received Ctrl+C. Stopping {self.code} gracefully...")
        logger.info(f"Received Ctrl+C. Stopping {self.code} gracefully...")

        # Set the running flag to False to exit the main loop
        self.running = False

    # Spool up the airport as a server, process passengers at that airport/server
    def run(self):
        # Create a UDP socket as the server
        # AF_INET indicates IPv4 addresses can be used.
        # SOCK_DGRAM: with connectionless service for datagrams
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Bind the socket to a specific address and port
            s.bind(('localhost', self.mapping.get(self.code)))
            s.settimeout(5)


            print(f"{self.code} initialized on port {self.mapping.get(self.code)}")
            logger.info(f"{self.code} initialized on port {self.mapping.get(self.code)}")

            while self.running:
                try:
                    data,addr = s.recvfrom(1024)
                    passenger = json.loads(data)

                    # Process passenger 
                    # Case 1: airport is the destination
                    if passenger['destination'] == self.code:
                        print(f"Passenger {passenger['fname']} {passenger['lname']} arrived at {self.code}")
                        logger.info(f"Passenger {passenger['fname']} {passenger['lname']} arrived at {self.code}") 
                    
                    # Case 2: airport is the layover airport
                    elif passenger['layover'] == self.code:
                        print(f"Passenger {passenger['fname']} {passenger['lname']} at layover in {self.code}")
                        logger.info(f"Passenger {passenger['fname']} {passenger['lname']} at layover in {self.code}")

                        # Forward to the next airport
                        self.forward_passenger(passenger, passenger['destination'])

                    # Case 3: airport is the origin and there is no layover
                    elif passenger['origin'] == self.code and passenger['layover'] == None:
                        print(f"Passenger {passenger['fname']} {passenger['lname']} leaving airport at {self.code}.")
                        logger.info(f"Passenger {passenger['fname']} {passenger['lname']} leaving airport at {self.code}.")
                        self.forward_passenger(passenger, passenger['destination'])
                    
                    # Case 4: airport is the origin and there is a layover
                    elif passenger['origin'] == self.code and passenger['layover'] != None:
                        print(f"Passenger {passenger['fname']} {passenger['lname']} leaving airport at {self.code} for layover at {passenger['layover']}.")
                        logger.info(f"Passenger {passenger['fname']} {passenger['lname']} leaving airport at {self.code} for layover at {passenger['layover']}.")
                        
                        # Forward to the next airport
                        self.forward_passenger(passenger, passenger['layover'])    
                
                except socket.timeout:
                    pass


            # Close the socket after exiting the while True loop
            s.close()

    def forward_passenger(self, passenger, airport_code):
        dest_port = self.mapping.get(airport_code)
        if dest_port:
            # Create a UDP socket as the client
            # AF_INET indicates IPv4 addresses can be used.
            # SOCK_DGRAM: with connectionless service for datagrams
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                # Convert passenger dictionary to json object, encode it as utf-8, and send it to destination airport
                s.sendto(json.dumps(passenger).encode('utf-8'), ('localhost', dest_port))

            # Close the socket
            s.close()


if __name__ == "__main__":

    # Use arpgparse library to make sending passengers through the command line easier and more customizable
    parser = argparse.ArgumentParser(description="Run airport node")
    parser.add_argument("code", help="IATA code of the airport")
    args = parser.parse_args()

    # Initialize instance of Airport object with the airport code input by the user
    airport = Airport(args.code)
    airport.run()