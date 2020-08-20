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
        currentUser = get_jwt_identity()
        bookmarkedLinks = DbHandler.getLinks(currentUser)
        bookmarkedLinksNames = []
        for link in bookmarkedLinks:
            bookmarkedLinksNames.append(link.getAddressName())
        return make_response(jsonify(bookmarked_links=bookmarkedLinksNames), 200)
