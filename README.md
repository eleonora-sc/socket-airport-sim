# socket-airport-sim

Requirements
Python 3.10
pip 23.2.1
standard (built in) libraries: socket, json, logging, signal
external libraries: argparse==1.4.0 (you can run ‘pip install -r requirements.txt’ to install the argparse library)

Running the code:
1. Open at least 3 different terminals, one for each airport that you want to use (minimum 2) and one to initialize the passengers that need to be routed. Navigate to the directory with the files in each terminal.

2. In each terminal that is used to initialize the airports, type: 'python airport.py {code of airport}'
The different airport codes are: ANC, FAI, SEA, BRW, OTZ, SCC, BET, JNU
ANC, FAI and SEA are hubs. BRW, OTZ, SCC, BET, and JNU are spokes.
You must have at least one hub airport.

3. Use the last terminal to route passengers. To do that type: 'python route_passenger.py {first name of passenger} {last name of passenger} {origin airport code} {destination airport code}’. 
As an optional argument you can append --layover {layover airport code}
You can initialize and route one passenger per command.

4. If you would like to gracefully close the airport server, you can type CTRL+C in each airport.py console.
