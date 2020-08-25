# Add or return bookmarked links for signed-in user

from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler
from common.Link import Link

parser = reqparse.RequestParser(bundle_errors=True)


class Links(Resource):
    @jwt_required
    @swag_from('../yml/links_get.yml')
    def get(self):
        current_user = get_jwt_identity()
        bookmarked_links = DbHandler.get_links(current_user)
        bookmarked_links_names = []
        for link in bookmarked_links:
            bookmarked_links_names.append(link.get_address_name())
        return make_response(
            jsonify(bookmarked_links=bookmarked_links_names), 200
        )

    @jwt_required
    @swag_from('../yml/links_post.yml')
    def post(self):
        parser.add_argument('address_name', type=str, required=True)
        # Get a list of strings {'categories': ['X', 'Y', 'Z']}
        parser.add_argument(
            'categories', type=str,
            action='append'
        )

        args = parser.parse_args()

        current_user = get_jwt_identity()
        address_name = args['address_name']
        categories = args['categories']
        new_link = Link(address_name, categories)

        if DbHandler.append_new_link(current_user, new_link) == 0:
            return make_response(
                jsonify(address_name=address_name, categories=categories),
                200
            )
        else:
            return make_response(
                jsonify(msg="Failed to add new link"), 500
            )

    @jwt_required
    def delete(self):
        parser.add_argument('address_name', type=str, required=True)

        args = parser.parse_args()
        current_user = get_jwt_identity()
        address_name = args['address_name']

        if DbHandler.remove_link(current_user, address_name) == 0:
            return make_response(
                jsonify(address_name=address_name), 200
            )
        else:
            return make_response(
                jsonify(msg="Link doesn't exists"), 404
            )
