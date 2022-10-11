from email import message
import re
import grpc
from concurrent import futures
import movie_pb2
import movie_pb2_grpc
import json
from google.protobuf.json_format import MessageToJson

EMPTY_MOVIE_DATA = movie_pb2.MovieData(title="",
                                       rating=float("nan"),
                                       director="",
                                       id="")

class MovieServicer(movie_pb2_grpc.MovieServicer):

    def __init__(self):
        with open('{}/data/movies.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["movies"]


    def GetMovieByID(self, request, context):
        for movie in self.db:
            if movie['id'] == request.id:
                print("Movie found!")
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        return movie_pb2.MovieData(title="", rating=0.0, director="", id="")
    
    def GetListMovies(self, request, context):
        for movie in self.db:
            yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])

    def GetMovieByTitle(self, request, context):
        for movie in self.db:
            if movie['title'] == request.title:
                print("Movie found!")
                return movie_pb2.MovieData(title=movie['title'],
                                           rating=float(movie['rating']),
                                           director=movie['director'],
                                           id=movie['id'])
        return EMPTY_MOVIE_DATA

    def CreateMovie(self, request, context):

        for movie in self.db:
            if str(movie['id']) == str(request.id):
                return movie_pb2.FeedbackMessage(
                    message='movie ID already exists', movie=EMPTY_MOVIE_DATA)

        movie_json = json.loads(MessageToJson(request))
        self.db.append(movie_json)
        return movie_pb2.FeedbackMessage(
            message='movie added', movie=movie_pb2.MovieData(**movie_json))  

    def UpdateMovieRating(self, request, context):
        if request.id:
            for movie in self.db:
                if str(movie['id']) == str(request.id):
                    movie['rating'] = float(request.rating)
                    return movie_pb2.FeedbackMessage(
                        message='movie rating updated',
                        movie=movie_pb2.MovieData(**movie))
            return movie_pb2.FeedbackMessage(message='movie not found',
                                             movie=EMPTY_MOVIE_DATA)
        if request.title:
            for movie in self.db:
                if str(movie['title']) == str(request.title):
                    movie['rating'] = float(request.rating)
                    return movie_pb2.FeedbackMessage(
                        message='movie rating updated',
                        movie=movie_pb2.MovieData(**movie))
            return movie_pb2.FeedbackMessage(message='movie not found',
                                             movie=EMPTY_MOVIE_DATA)
        return movie_pb2.FeedbackMessage(
            message='needs at least one of id or title', movie=EMPTY_MOVIE_DATA)

    def RemoveMovie(self, request, context):
        for movie in self.db:
            if str(movie['id']) == str(request.id):
                self.db.remove(movie)
                return movie_pb2.FeedbackMessage(
                    message='movie removed', movie=movie_pb2.MovieData(**movie))

        return movie_pb2.FeedbackMessage(message='movie not found',
                                         movie=EMPTY_MOVIE_DATA)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movie_pb2_grpc.add_MovieServicer_to_server(MovieServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
