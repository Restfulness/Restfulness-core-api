from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from common.DbHandler import DbHandler

import json

# Load config file
with open('config.json', mode='r') as config_file:
    MAX_ACTIVITIES_PER_PAGE = json.load(config_file).get('pagination', {}).\
        get('maximum_activities_per_page')

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('date_from', type=str)
parser.add_argument('page', type=int, location='args')
parser.add_argument('page_size', type=int, location='args')


class Activity(Resource):
    @jwt_required
    @swag_from('../../../yml/socializing/activity_get.yml')
    def post(self):
        """ Return users activities paginated from a special date (If provided).
        """
        args = parser.parse_args(strict=True)
        date_from = args['date_from']
        page = args['page']
        page_size = args['page_size']

        if page and page_size:
            if page_size > MAX_ACTIVITIES_PER_PAGE:
                return make_response(
                    jsonify(msg="Requested page size " +
                            "is larger than our max limit!"),
                    400
                )
            activity_list = DbHandler.get_users_activity_list(page, page_size,
                                                              date_from)
        else:
            activity_list = DbHandler.get_users_activity_list(
                date_from=date_from)

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
