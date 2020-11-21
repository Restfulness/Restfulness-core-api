from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler


class LinksGetter(Resource):
    @jwt_required
    @swag_from('../../yml/links_get.yml')
    def get(self, id=None):
        """ If client requests for /links will get paginated links;
        else if requests for /links/[ID] will get specified link.
        """
        current_user_username = get_jwt_identity()
        args = request.args
        # TODO: Validation required
        if args.get('page', None) and args.get('page_size', None):
            page = int(args.get('page'))
            page_size = int(args.get('page_size'))
            links_list = DbHandler.get_links(current_user_username, id, page, page_size)
        else:
            links_list = DbHandler.get_links(current_user_username, id)
        if links_list:
            return make_response(
                jsonify(links_list),
                200
            )
        else:
            return make_response(
                jsonify(msg="Link not found!"),
                404
            )
