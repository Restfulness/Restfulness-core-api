# Add or return bookmarked links for signed-in user

from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler
from common.Link import Link
from common.Category import Category

import validators


class Links(Resource):
    @jwt_required
    @swag_from('../yml/links_get.yml')
    def get(self):
        current_user_username = get_jwt_identity()
        current_user_object = DbHandler.get_user_object(
            username=current_user_username
        )

        return make_response(
            jsonify(
                bookmarked_links_id=[
                    link.id for link in current_user_object.links
                ]
            ), 200
        )

    @jwt_required
    @swag_from('../yml/links_post.yml')
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('url', type=str, required=True)
        # Get a list of strings {'categories': ['X', 'Y', 'Z']}
        parser.add_argument(
            'categories', type=str,
            action='append', required=True
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
        category_objects = [
            Category(
                name=category_name,
                owner=new_link
            )
            for category_name in categories_name
        ]

        if (
            DbHandler.append_new_link(new_link=new_link) == "OK" and
            DbHandler.append_new_categories(
                categories=category_objects
            ) == "OK"
        ):
            return make_response(
                jsonify(url=url, categories=categories_name),
                200
            )
        else:
            return make_response(
                jsonify(msg="Failed to add new link"), 500
            )

    @jwt_required
    @swag_from('../yml/links_delete.yml')
    def delete(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('link_id', type=int, required=True)
        args = parser.parse_args()

        link_id = args['link_id']

        current_user_username = get_jwt_identity()

        remove_status = DbHandler.remove_link(current_user_username, link_id)
        if remove_status == "OK":
            return make_response(
                jsonify(msg="Link removed successfully.", link_id=link_id),
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
