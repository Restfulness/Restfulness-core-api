from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
# from flasgger import swag_from

from common.DbHandler import DbHandler

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('date_from', type=str)


class LinksByUserId(Resource):
    @jwt_required
    # @swag_from('../../yml/links_get.yml')
    def post(self, id):
        """ Return links related to specific user ID, if user is public.
        Also if you provide special date, it will return links from that time.
        """
        args = parser.parse_args()
        date_from = args['date_from']

        links_list = DbHandler.get_public_user_links(id, date_from)
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
