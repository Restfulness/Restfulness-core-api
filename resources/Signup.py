from flask_restful import reqparse, Resource
from flask import jsonify, make_response

from common.DbHandler import DbHandler

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', type=str, required=True)
parser.add_argument('password', type=str, required=True)

class Signup(Resource):
    def post(self):
        args = parser.parse_args()

        username = args["username"]
        password = args["password"]

        validateSignUp = DbHandler.addNewUser(username, password)
        
        returnMessage = ""
        if validateSignUp == 0:
            returnMessage = make_response(jsonify(username=username, msg="User created"), 200)
        elif validateSignUp == 1:
            returnMessage = make_response(jsonify({"msg": "Username is exists"}), 401)

        return returnMessage
