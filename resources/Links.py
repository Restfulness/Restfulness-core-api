# Add or return bookmarked links for signed-in user

from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from common.DbHandler import DbHandler
from common.Link import Link

import validators


class Links(Resource):
    @jwt_required
    @swag_from('../yml/links_get.yml')
    def get(self):
        current_user_username = get_jwt_identity()
        current_user_object = DbHandler.get_user_object(
            username=current_user_username
        )

        bookmarked_links_ids = []
        for link in current_user_object.links:
            bookmarked_links_ids.append(link.id)
        return make_response(
            jsonify(bookmarked_links_id=bookmarked_links_ids), 200
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
        categories = args['categories']
        # Validate link
        if not validators.url(url):
            return make_response(
                jsonify(msg="Link is not valid. Valid link looks like: " +
                        "http://example.com or https://example.com"), 400
            )

        current_user_object = DbHandler.get_user_object(
            username=current_user_username
        )
        categories_str = ','.join(categories)
        new_link = Link(
            url=url,
            owner=current_user_object,
            categories=categories_str
        )

        if DbHandler.append_new_link(new_link=new_link) == 0:
            return make_response(
                jsonify(url=url, categories=categories),
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
        if remove_status == 0:
            return make_response(
                jsonify(msg="Link removed successfully.", link_id=link_id),
                200
            )
        elif remove_status == 1:
            return make_response(
                jsonify(msg="You don't have permission to " +
                        "remove this link"), 403
            )
        elif remove_status == 2:
            return make_response(
                jsonify(msg="Link doesn't exists!"), 406
            )
