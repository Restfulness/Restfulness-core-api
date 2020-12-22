from flask_restful import reqparse, Resource
from flask import jsonify, make_response

from flasgger import swag_from

from src.ResetPasswordCore import ResetPasswordCore

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, required=True)


class ForgetPassword(Resource):
    @swag_from('../../../yml/forget_password/forget_password.yml')
    def post(self):
        args = parser.parse_args()
        username = args['username']

        hash_data = ResetPasswordCore.get_n_digit_auth_code(username)

        return_message = ''
        if hash_data == 'USER_NOT_FOUND':
            return_message = make_response(
                jsonify({'msg': 'Username not found'}), 404
            )
        else:
            return_message = make_response(
                jsonify({'hashed_data': hash_data}), 200
            )

        return(return_message)
