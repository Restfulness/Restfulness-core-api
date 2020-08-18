from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.Login import Login
from resources.Signup import Signup
from resources.Links import Links

app = Flask(__name__)
api = Api(app)

app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Routes
api.add_resource(Login, '/login')
api.add_resource(Signup, '/signup')
api.add_resource(Links, '/links')

if __name__ == '__main__':
    app.run()
