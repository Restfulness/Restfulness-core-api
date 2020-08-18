from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from resources.TodoList import TodoList
from resources.Login import Login
from resources.Signup import Signup

app = Flask(__name__)
api = Api(app)

app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Routes
api.add_resource(TodoList, '/todos')
api.add_resource(Login, '/login')
api.add_resource(Signup, '/signup')


if __name__ == '__main__':
    app.run()
