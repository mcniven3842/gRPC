# TP2 gRPC

## Info
The project consists of 4 services, the services are:
* [movie]
* [showtime]
* [booking]
* [user]

The files inside the folder are:

* [Main server file (*.py)]
* [Dockerfile to build service image]
*[Python library requirements (requirements.txt)]
*[data folder with the .json file that holds the service data]
*[protos folder with the .proto file of the service describing its stubs]
## Technologies
***
* [Python]: Version 3.10 
* [Docker]

## Implementation
cd movie
python movie.py
cd showtime
python showtime.py
cd booking
python booking.py
cd user
python3 user.py [-H HOST] -p PORT

##Test
cd client
python3.10 client.py

inside the terminal run the following command:
docker-compose up
