from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler
from common.Link import Link

import validators


class Links(Resource):
    @jwt_required
    @swag_from('../../yml/links_add.yml')
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('url', type=str, required=True)
        # Get a list of strings {'categories': ['X', 'Y', 'Z']}
        parser.add_argument(
            'categories', type=str,
            action='append'
        )

        args = parser.parse_args()

        current_user_username = get_jwt_identity()
        url = args['url']
        categories_name = args['categories']
        # Validate link
        if not validators.url(url):
            return make_response(
                jsonify(msg="Link is not valid. Valid link looks like: " +
                        "http://example.com or https://example.com"), 400
            )

        current_user_object = DbHandler.get_user_object(
            username=current_user_username
        )
        new_link = Link(
            url=url,
            owner=current_user_object
        )

        if DbHandler.append_new_link(
            new_link=new_link,
            categories_name=categories_name
        ) == "OK":
            return make_response(
                jsonify(id=new_link.id), 200
            )
        else:
            return make_response(
                jsonify(msg="Failed to add new link"), 500
            )

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

    @jwt_required
    @swag_from('../../yml/links_get.yml')
    def get(self, id=None):
        """ If client requests for /links will get whole links;
        else if requests for /links/[ID] will get specified link.
        NOTE: -1 is used as sentinel value
        """
        current_user_username = get_jwt_identity()
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
