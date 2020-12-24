from flask_restful import Resource
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from src.DbHandler import DbHandler


class CategoriesGetter(Resource):
    @jwt_required
    @swag_from('../../yml/categories_get.yml')
    def get(self, id=None):
        """ If client requests for /categories will get whole categories;
        else if requests for /categories/[ID] will get specified category.
        """
        current_user_username = get_jwt_identity()
        categories_list = DbHandler.get_categories(current_user_username, id)
        if categories_list == 'ID_NOT_FOUND':
            return make_response(
                jsonify(msg="Category not found!"),
                404
            )
        else:
            return make_response(
                jsonify(categories_list),
                200
            )
