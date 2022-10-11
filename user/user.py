from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound
from collections import defaultdict
from datetime import datetime
from google.protobuf.json_format import MessageToJson

import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import movie_pb2
import movie_pb2_grpc

app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

BOOKING = 'localhost:3003'
MOVIE = 'localhost:3001'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route('/users', methods=['GET'])
def get_users():
    return make_response(jsonify(users), 200)


@app.route('/users/<userid>', methods=['GET'])
def get_user_by_id(userid):
    for user in users:
        if str(user['id']) == str(userid):
            res = make_response(jsonify(user), 200)
            return res
    return make_response(jsonify({'error': 'User ID not found'}), 404)


@app.route('/users/<userid>', methods=['POST'])
def create_user(userid):
    for user in users:
        if str(user['id']) == str(userid):
            return make_response(jsonify({'error': 'user already exists'}), 409)

    body = request.get_json()
    name = body['name']

    user = {
        'id': userid,
        'name': name,
        'last_active': int(datetime.now().strftime('%Y%m%d')),
    }
    users.append(user)
    return make_response(jsonify(user), 201)


@app.route('/users/<userid>', methods=['PUT'])
def update_user(userid):
    body = request.get_json()
    for user in users:
        if str(user['id']) == str(userid):
            user['name'] = body.get('name', user['name'])
            user['last_active'] = body.get('last_active', user['last_active'])
            return make_response(jsonify(user), 200)

    return make_response(jsonify({'error': 'User ID not found'}), 404)


@app.route('/users/<userid>/bookings', methods=['GET'])
def get_user_bookings_by_id(userid):
    for user in users:
        if str(user['id']) == str(userid):
            break
    else:
        return make_response(jsonify({'error': 'User ID not found'}), 404)

    with grpc.insecure_channel(BOOKING) as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        userId = booking_pb2.UserId(userid=userid)
        response = stub.GetBookingByUserId(userId)
        bookings_by_date = response.booking.dates

    dates_by_movie = defaultdict(list)
    for booking in bookings_by_date:
        for movieid in booking.movies:
            dates_by_movie[movieid].append(booking.date)

    bookings = []
    with grpc.insecure_channel(MOVIE) as channel:
        stub = movie_pb2_grpc.MovieStub(channel)
        for movieid, dates in dates_by_movie.items():
            response = stub.GetMovieByID(movie_pb2.MovieID(id=movieid))
            bookings.append(
                json.loads(MessageToJson(response)) | {'dates': dates})

    return make_response(jsonify(bookings), 200)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
