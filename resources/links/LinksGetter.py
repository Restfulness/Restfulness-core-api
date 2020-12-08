from flask_restful import Resource
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler


class LinksGetter(Resource):
    @jwt_required
    @swag_from('../../yml/links_get.yml')
    def get(self, id=None):
        """ If client requests for /links will get whole links;
        else if requests for /links/[ID] will get specified link.
        """
        user_id = DbHandler.get_user_id(get_jwt_identity())
        links_list = DbHandler.get_links(user_id, id)
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
