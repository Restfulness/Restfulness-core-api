from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from src.DbHandler import DbHandler

import json

# Load config file
with open('config.json', mode='r') as config_file:
    MAX_LINKS_PER_PAGE = json.load(config_file).get('pagination', {}).\
        get('maximum_links_per_page')


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('date_from', type=str)
parser.add_argument('page', type=int, location='args')
parser.add_argument('page_size', type=int, location='args')


class LinksByUserId(Resource):
    @jwt_required
    @swag_from('../../yml/links_by_user_id.yml')
    def post(self, id):
        """ Return links related to specific user ID, if user is public.
        Also if you provide special date, it will return links from that time.
        """
        args = parser.parse_args()
        date_from = args['date_from']
        page = args['page']
        page_size = args['page_size']

        if page and page_size:
            if page_size > MAX_LINKS_PER_PAGE:
                return make_response(
                    jsonify(msg="Requested page size " +
                            "is larger than our max limit!"),
                    400
                )
            links_list = DbHandler.get_public_user_links(id, page, page_size,
                                                         date_from)
        else:
            links_list = DbHandler.get_public_user_links(id,
                                                         date_from=date_from)

        if links_list == 'USER_NOT_FOUND':
            return make_response(
                jsonify(msg='User not found!'),
                404
            )
        elif links_list == 'LINK_NOT_FOUND':
            return make_response(
                jsonify(msg='Link not found!'),
                404
            )
        elif links_list == 'USER_NOT_PUBLIC':
            return make_response(
                jsonify(msg='User is not public!'),
                403
            )
        elif links_list == 'WRONG_DATE_FORMAT':
            return make_response(
                jsonify(msg='Input date does not match format' +
                        '"YYYY-MM-DD hh:mm"'),
                400
            )
        else:
            return make_response(
                jsonify(links_list),
                200
            )
