# Add or return bookmarked links for signed-in user

from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler
from common.Link import Link

import validators


class AddLink(Resource):
    @jwt_required
    @swag_from('../yml/links_post.yml')
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('url', type=str, required=True)
        # Get a list of strings {'categories': ['X', 'Y', 'Z']}
        parser.add_argument(
            'categories', type=str,
            action='append', required=True
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

        current_user_object = DbHandler.get_user_object(
            username=current_user_username
        )
        new_link = Link(
            url=url,
            owner=current_user_object
        )

        if DbHandler.append_new_link(
            new_link=new_link,
            categories_name=categories_name
        ) == "OK":
            return make_response(
                jsonify(id=new_link.id), 200
            )
        else:
            return make_response(
                jsonify(msg="Failed to add new link"), 500
            )
