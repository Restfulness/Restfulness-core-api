from flask_restful import reqparse, Resource
# from flask import jsonify, make_response

# from flasgger import swag_from

from common.ResetPasswordCore import ResetPasswordCore

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, required=True)


class ForgetPassword(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['username']

        ResetPasswordCore.get_8_digit_auth_code(username)
