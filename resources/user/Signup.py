from flask_restful import reqparse, Resource
from flask import jsonify, make_response

from flasgger import swag_from
import validators

from common.DbHandler import DbHandler

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, required=True)
parser.add_argument('password', type=str, required=True)


class Signup(Resource):
    @swag_from('../../yml/signup.yml')
    def post(self):
        args = parser.parse_args()

        username = args["username"]
        password = args["password"]

        # Validate if username is Email or not
        if not validators.email(username):
            return make_response(
                jsonify(msg="Username should be an valid Email."), 400
            )

        validate_sign_up = DbHandler.add_new_user(username, password)

        return_message = ""
        if validate_sign_up == "OK":
            return_message = make_response(
                jsonify(username=username, msg="User created"), 200
            )
        elif validate_sign_up == "USER_EXISTS":
            return_message = make_response(
                jsonify({"msg": "Username exists"}), 403
            )

        return return_message
