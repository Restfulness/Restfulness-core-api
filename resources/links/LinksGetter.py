from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from src.DbHandler import DbHandler
import json

# Load config file
with open('config.json', mode='r') as config_file:
    MAX_LINKS_PER_PAGE = json.load(config_file).get('pagination', {}).\
        get('maximum_links_per_page')


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('page', type=int, location='args')
parser.add_argument('page_size', type=int, location='args')


class LinksGetter(Resource):
    @jwt_required
    @swag_from('../../yml/links_get.yml')
    def get(self, id=None):
        """ If client requests for /links will get paginated links;
        else if requests for /links/[ID] will get specified link.
        """
        args = parser.parse_args()
        user_id = DbHandler.get_user_id(get_jwt_identity())
        page = args['page']
        page_size = args['page_size']

        if page and page_size:
            if page_size > MAX_LINKS_PER_PAGE:
                return make_response(
                    jsonify(msg="Requested page size " +
                            "is larger than our max limit!"),
                    400
                )
            links_list = DbHandler.get_links(user_id, id, page, page_size)
        else:
            links_list = DbHandler.get_links(user_id, id)
        if links_list == 'LINK_NOT_FOUND':
            return make_response(
                jsonify(msg="Link not found!"),
                404
            )
        else:
            return make_response(
                jsonify(links_list),
                200
            )
