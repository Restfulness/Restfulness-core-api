from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from common.DbHandler import DbHandler

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('date_from', type=str, required=True)


class Activity(Resource):
    @jwt_required
    @swag_from('../../../yml/socializing/activity_get.yml')
    def post(self):
        """ Return users activities from a special date. """
        args = parser.parse_args()
        date_from = args['date_from']

        activity_list = DbHandler.get_users_activity_list(date_from)
        if activity_list == 'WRONG_FORMAT':
            return make_response(
                jsonify(
                    msg="Input does not match format 'YYYY-MM-DD hh:mm'"
                ),
                400
            )
        elif activity_list == 'NOT_FOUND':
            return make_response(
                jsonify(msg="Didn't found any activity from that time"),
                404
            )
        else:
            return make_response(
                jsonify(activity_list),
                200
            )
