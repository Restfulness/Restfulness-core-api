from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
import json

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

# Load config file
with open('config.json', mode='r') as config_file:
    CONFIG = json.load(config_file)

# Routes
api.add_resource(Login, CONFIG['routes']['user']['login'])
api.add_resource(Signup, CONFIG['routes']['user']['signup'])
api.add_resource(Links, CONFIG['routes']['user']['links'])

if __name__ == '__main__':
    app.run()
