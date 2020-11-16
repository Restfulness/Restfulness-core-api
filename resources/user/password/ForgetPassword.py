from flask_restful import reqparse, Resource
from flask import jsonify, make_response

from flasgger import swag_from

from common.DbHandler import DbHandler

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, required=True)


class ForgetPassword(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['username']
        print(DbHandler.get_user_email(username))
