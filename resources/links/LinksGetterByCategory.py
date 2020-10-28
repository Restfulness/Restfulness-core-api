from flask_restful import Resource
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler


class LinksGetterByCategory(Resource):
    @jwt_required
    @swag_from('../../yml/links_get_category.yml')
    def get(self, id):
        """ Return links by special Category ID """
        current_user_username = get_jwt_identity()
        links_list = DbHandler.get_links_by_category(current_user_username, id)
        if links_list == 'CATEGORY_NOT_FOUND':
            return make_response(
                jsonify(msg="Category not found!"),
                404
            )
        else:
            return make_response(
                jsonify(links_list),
                200
            )
