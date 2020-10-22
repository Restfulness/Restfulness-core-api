from flask_restful import Resource
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler


class LinksDeleter(Resource):
    @jwt_required
    @swag_from('../../yml/links_delete.yml')
    def delete(self, id):
        current_user_username = get_jwt_identity()

        remove_status = DbHandler.remove_link(current_user_username, id)
        if remove_status == "OK":
            return make_response(
                jsonify(msg="Link removed successfully.", link_id=id),
                200
            )
        elif remove_status == "USER_IS_NOT_OWNER":
            return make_response(
                jsonify(msg="You don't have permission to " +
                        "remove this link"), 403
            )
        elif remove_status == "ID_NOT_FOUND":
            return make_response(
                jsonify(msg="Link doesn't exists!"), 404
            )
