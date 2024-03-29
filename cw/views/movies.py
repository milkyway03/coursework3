from flask_restx import abort, Namespace, Resource, reqparse

from cw.exceptions import ItemNotFound
from cw.services import MoviesService
from cw.setup_db import db
from cw.tools.security import auth_required

movies_ns = Namespace("movies")
parser = reqparse.RequestParser()
parser.add_argument('page', type=int)
parser.add_argument('status', type=str)


@movies_ns.route("/")
class MoviesView(Resource):
    @movies_ns.expect(parser)
    @auth_required
    @movies_ns.response(200, "OK")
    def get(self):
        req_args = parser.parse_args()
        if any(req_args.values()):
            return MoviesService(db.session).get_filter_movies(req_args)
        else:
            return MoviesService(db.session).get_all_movies()


@movies_ns.route("/<int:movie_id>")
class MovieView(Resource):
    @auth_required
    @movies_ns.response(200, "OK")
    @movies_ns.response(484, "Movie is not found")
    def get(self, movie_id: int):
        try:
            return MoviesService(db.session).get_item_by_id(movie_id)
        except ItemNotFound:
            abort(404, message="Movie is not found")
