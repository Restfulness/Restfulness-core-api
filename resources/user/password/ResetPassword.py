from flask_restful import reqparse, Resource
from flask import jsonify, make_response

from flasgger import swag_from

from common.ResetPasswordCore import ResetPasswordCore

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('reset_password_token', type=str, required=True)
parser.add_argument('new_password', type=str, required=True)


class ResetPassword(Resource):
    @swag_from('../../../yml/forget_password/reset_password.yml')
    def post(self):
        args = parser.parse_args()
        token = args['reset_password_token']
        new_password = args['new_password']

        status = ResetPasswordCore.reset_password(token, new_password)

        return_message = ''
        if status == 'EXPIRED':
            return_message = make_response(
                jsonify({'msg': 'Token expired!'}), 401
            )
        elif status == 'INVALID_TOKEN':
            return_message = make_response(
                jsonify({'msg': 'Token invalid!'}), 401
            )
        elif status == 'FAILED':
            return_message = make_response(
                jsonify({'msg': 'Failed due to server error'}), 500
            )
        elif status == 'OK':
            return_message = make_response(
                jsonify({'msg': 'Password reseted successfully.'}), 200
            )

        return(return_message)
