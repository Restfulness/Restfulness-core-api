from flask_restful import Resource
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
# from flasgger import swag_from

from src.DbHandler import DbHandler


class Profile(Resource):
    @jwt_required
    # @swag_from('../../yml/publicity_put.yml')
    def delete(self):
        """ Delete current user's profile """
        current_user_username = get_jwt_identity()

        status = DbHandler.delete_user_profile(current_user_username)
        if status == 'OK':
            return make_response(
                jsonify(msg="User's profile deleted."),
                200
            )
        else:
            return make_response(
                jsonify(msg="Server Error!"),
                500
            )
