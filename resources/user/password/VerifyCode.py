from flask_restful import reqparse, Resource
from flask import jsonify, make_response

from flasgger import swag_from

from common.ResetPasswordCore import ResetPasswordCore

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('hashed_data', type=str, required=True)
parser.add_argument('user_input', type=str, required=True)


class VerifyCode(Resource):
    @swag_from('../../../yml/forget_password/verify_code.yml')
    def post(self):
        args = parser.parse_args()
        hashed_data = args['hashed_data']
        user_input = args['user_input']

        reset_token = ResetPasswordCore.get_password_reset_token(
            hashed_data, user_input)

        return_message = ''
        if reset_token == 'EXPIRED':
            return_message = make_response(
                jsonify({'msg': 'Token expired!'}), 401
            )
        elif reset_token == 'INVALID_TOKEN':
            return_message = make_response(
                jsonify({'msg': 'Token invalid!'}), 401
            )
        elif reset_token == 'INVALID_CODE':
            return_message = make_response(
                jsonify({'msg': 'User inputed code is incorrect'}), 400
            )
        else:
            return_message = make_response(
                jsonify({'reset_password_token': reset_token}), 200
            )

        return(return_message)
