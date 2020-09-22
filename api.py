from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import json

from resources.user.Login import Login
from resources.user.Signup import Signup
from resources.links.AddLink import AddLink
from resources.links.DeleteLink import DeleteLink
from resources.links.GetLink import GetLink


from db import db

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)
jwt = JWTManager(app)


# Load config file
with open('config.json', mode='r') as config_file:
    CONFIG = json.load(config_file)

# Database connection
database_username = CONFIG.get('database', {}).get('username')
database_password = CONFIG.get('database', {}).get('password')
database_server = CONFIG.get('database', {}).get('server')
database_db = CONFIG.get('database', {}).get('db')
if CONFIG.get('database', {}).get('production'):
    database_uri = (f'mysql+pymysql://{database_username}:{database_password}@'
                    f'{database_server}/{database_db}')
else:
    database_uri = 'sqlite:///tests/test.db'

# Configs
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Routes
api.add_resource(
    Login, CONFIG.get('routes', {}).get('user', {}).get('login')
)
api.add_resource(
    Signup, CONFIG.get('routes', {}).get('user', {}).get('signup')
)
api.add_resource(
    AddLink, CONFIG.get('routes', {}).get('links', {}).get('add')
)
api.add_resource(
    GetLink, CONFIG.get('routes', {}).get('links', {}).get('get_id'),
    CONFIG.get('routes', {}).get('links', {}).get('get_all')
)
api.add_resource(
    DeleteLink, CONFIG.get('routes', {}).get('links', {}).get('delete')
)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
