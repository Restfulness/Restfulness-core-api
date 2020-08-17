from flask_restful import reqparse, Resource
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token
from flask import jsonify, make_response
import json

from common.User import User
from common.Link import Link

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

class Login(Resource):
    def post(self):
        args = parser.parse_args()
        
        username = args["username"]
        password = args["password"]
        
        links = [
            Link("www.stackoverflow.com", ["programming"]),
            Link("www.geeksforgeeks.com", ["programming", "learning"])
        ]
        users = [
            User(1, 'user1', 'zanjan', links[0]),
            User(2, 'user2', 'berlin', links),
        ]
        username_table = {u.username: u for u in users}
        user = username_table.get(username, None)
        
        if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
            #Identity can be any data that is json serializable
            access_token = create_access_token(identity=username)
            return make_response(jsonify(access_token=access_token), 200)
        else:
            return make_response(jsonify({"msg": "Bad username or password"}), 401)

