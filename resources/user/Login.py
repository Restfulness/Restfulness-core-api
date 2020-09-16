from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token
from flask import jsonify, make_response

from flasgger import swag_from

from common.DbHandler import DbHandler

# Login API request parser
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, required=True)
parser.add_argument('password', type=str, required=True)


class Login(Resource):
    @swag_from('../../yml/login.yml')
    def post(self):
        args = parser.parse_args()

        username = args["username"]
        password = args["password"]

        # Check if username and password are correct
        user = DbHandler.validate_login(username, password)

        return_message = ""
        if user:
            # Identity can be any data that is json serializable
            access_token = create_access_token(identity=username)
            return_message = make_response(
                jsonify(access_token=access_token), 200
            )
        else:
            return_message = make_response(
                jsonify({"msg": "Bad username or password"}), 401
            )
        return return_message
