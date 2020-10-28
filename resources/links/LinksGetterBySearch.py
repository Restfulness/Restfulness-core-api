from flask_restful import Resource
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler


class LinksGetterBySearch(Resource):
    @jwt_required
    #@swag_from('../../yml/links_get_category.yml')
    def get(self, pattern):
        """ Return links that contains special key word """
        current_user_username = get_jwt_identity()
        links_list = DbHandler.get_links_by_pattern(current_user_username,
                                                    pattern)
        if links_list == 'PATTERN_NOT_FOUND':
            return make_response(
                jsonify(msg="Pattern not found!"),
                404
            )
        else:
            return make_response(
                jsonify(links_list),
                200
            )
