# Add or return bookmarked links for signed-in user

from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler
from common.Link import Link

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('address_name', type=str)
# Get a list of strings {'categories': ['X', 'Y', 'Z']}
parser.add_argument(
    'categories', type=str,
    action='append'
)


class Links(Resource):
    @jwt_required
    @swag_from('../yml/links.yml')
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
    def post(self):
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
