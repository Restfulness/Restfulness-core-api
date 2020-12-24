from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from src.DbHandler import DbHandler

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'new_categories', type=str,
    action='append'
)


class LinksUpdateCategory(Resource):
    @jwt_required
    @swag_from('../../yml/links_update_category.yml')
    def put(self, id):
        """ Update categories related to Link ID. """
        current_user_username = get_jwt_identity()
        args = parser.parse_args()
        new_categories = args['new_categories']

        update_status = DbHandler.update_link_categories(
            current_user_username, new_categories, id)

        if update_status == 'LINK_NOT_FOUND':
            return make_response(
                jsonify(msg="Link ID not found!"),
                404
            )
        else:
            return make_response(
                jsonify(msg="Categories updated."),
                200
            )
