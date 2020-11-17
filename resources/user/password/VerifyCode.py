from flask_restful import reqparse, Resource
from flask import jsonify, make_response

# from flasgger import swag_from

from common.ResetPasswordCore import ResetPasswordCore

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('hashed_data', type=str, required=True)
parser.add_argument('user_input', type=str, required=True)


class VerifyCode(Resource):
    def post(self):
        args = parser.parse_args()
        hashed_data = args['hashed_data']
        user_input = args['user_input']

        ResetPasswordCore.get_password_reset_token(hashed_data, user_input)
