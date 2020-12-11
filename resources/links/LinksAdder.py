from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler

import validators


class LinksAdder(Resource):
    @jwt_required
    @swag_from('../../yml/links_add.yml')
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('url', type=str, required=True)
        # Get a list of strings {'categories': ['X', 'Y', 'Z']}
        parser.add_argument(
            'categories', type=str,
            action='append'
        )

        args = parser.parse_args()

        current_user_username = get_jwt_identity()
        url = args['url']
        categories_name = args['categories']
        # Validate link
        if not validators.url(url):
            return make_response(
                jsonify(msg="Link is not valid. Valid link looks like: " +
                        "http://example.com or https://example.com"), 400
            )

        link_id = DbHandler.append_new_link(current_user_username, url,
                                            categories_name)
        return make_response(
            jsonify(id=link_id), 200
        )
