from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from src.DbHandler import DbHandler


class Publicity(Resource):
    @jwt_required
    @swag_from('../../yml/publicity_put.yml')
    def put(self):
        """ Update user's publicity setting. """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('publicity', type=bool, required=True)
        args = parser.parse_args()

        current_user_username = get_jwt_identity()
        publicity = args['publicity']

        status = DbHandler.update_user_publicity(current_user_username,
                                                 publicity)
        if status == 'OK':
            return make_response(
                jsonify(msg="Publicity updated."),
                200
            )
        else:
            return make_response(
                jsonify(msg="Server Error!"),
                500
            )

    @jwt_required
    @swag_from('../../yml/publicity_get.yml')
    def get(self):
        """ Returns user's publicity. """
        current_user_username = get_jwt_identity()
        user_status = DbHandler.get_user_publicity(DbHandler.get_user_id(
            current_user_username
        ))

        return make_response(
                jsonify(publicity=user_status),
                200
            )
