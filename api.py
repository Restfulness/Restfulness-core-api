from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from common.Link import Link
from common.User import User

from resources.TodoList import TodoList
from resources.Login import Login

app = Flask(__name__)
api = Api(app)

app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)
"""
links = [
    Link("www.stackoverflow.com", ["programming"]),
    Link("www.geeksforgeeks.com", ["programming", "learning"])

]
users = [
    User(1, 'user1', 'zanjan', links[0]),
    User(2, 'user2', 'berlin', links),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        #Identity can be any data that is json serializable
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

"""
# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Login, '/login')


if __name__ == '__main__':
    app.run()
