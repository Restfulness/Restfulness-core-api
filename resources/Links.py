# Add or return bookmarked links for signed-in user

from flask_restful import Resource
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

from flasgger import swag_from

from common.DbHandler import DbHandler


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
