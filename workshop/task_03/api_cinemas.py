""""
Includes the endpoints for namespace cinamas
"""

from flask_restplus import Namespace, Resource, reqparse

from .data_structures import Cinema
from .db_access import MongoDBConnector

db_accessor = MongoDBConnector()

name_parser = reqparse.RequestParser()
name_parser.add_argument(name='cinema_contains',
                         default='',
                         required=False,
                         help='substr to be contained in the cinema name')

title_parser = reqparse.RequestParser()
title_parser.add_argument(name='title_contains',
                          default='',
                          required=False,
                          help='substr to be contained in the movie title')

exact_name_parser = reqparse.RequestParser()
exact_name_parser.add_argument(name='name',
                               required=True,
                               help='exact cinema name')

api = Namespace('cinemas',
                description='Retrieve information about cinemas and currently playing movies.')


@api.route('/names')
class CinemaNames(Resource):

    @api.expect(name_parser)
    def get(self):
        """
        Get Berlin cinema names
        """

        args = name_parser.parse_args()

        cinemas = db_accessor.read_distinct_cinemas(args['cinema_contains'])
        return cinemas


@api.route('/details')
class CinemaDetails(Resource):

    @api.expect(exact_name_parser)
    def get(self):
        """
        Get all details from a cinema
        """

        args = exact_name_parser.parse_args()

        cinema = db_accessor.read_cinema_details(args['name'])
        return cinema.to_dict() if type(cinema) == Cinema else dict()


@api.route('/shows')
class CinemaShows(Resource):

    @api.expect(exact_name_parser)
    def get(self):
        """
        Get all movie titles and times playing in a cinema
        """

        args = exact_name_parser.parse_args()

        shows = db_accessor.read_cinema_shows(args['name'])
        return shows


@api.route('/movie_times')
class MovieTimes(Resource):

    @api.expect(name_parser, title_parser)
    def get(self):
        """
        Get cinemas where movie is playing along with show times.
        """

        args_n = name_parser.parse_args()
        args_t = title_parser.parse_args()

        cinemamovies = db_accessor.read_showtimes(args_n['cinema_contains'],
                                                  args_t['title_contains'])
        return [cn.to_dict() for cn in cinemamovies]
