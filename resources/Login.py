from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token
from flask import jsonify, make_response

from common.DbHandler import DbHandler

# Login API request parser
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, required=True)
parser.add_argument('password', type=str, required=True)

class Login(Resource):
    def post(self):
        args = parser.parse_args()
        
        username = args["username"]
        password = args["password"]
        
        # Check if username and password are correct
        user = DbHandler.validateLogin(username, password)
        
        returnMessage = ""
        if user:
            #Identity can be any data that is json serializable
            access_token = create_access_token(identity=username)
            returnMessage = make_response(jsonify(access_token=access_token), 200)
        else:
            returnMessage = make_response(jsonify({"msg": "Bad username or password"}), 401)
        return returnMessage
