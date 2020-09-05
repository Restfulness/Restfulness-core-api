from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import json

from resources.Login import Login
from resources.Signup import Signup
from resources.Links import Links

from db import db

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)
jwt = JWTManager(app)


# Load config file
with open('config.json', mode='r') as config_file:
    CONFIG = json.load(config_file)

# Database connection
database_username = CONFIG['database']['username']
database_password = CONFIG['database']['password']
database_server = CONFIG['database']['server']
database_db = CONFIG['database']['db']
database_uri = (f'mysql+pymysql://{database_username}:{database_password}@'
                f'{database_server}/{database_db}')

# Configs
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Routes
api.add_resource(Login, CONFIG['routes']['user']['login'])
api.add_resource(Signup, CONFIG['routes']['user']['signup'])
api.add_resource(Links, CONFIG['routes']['user']['links'])


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    # from db import db  # Avoid circular import
    app.run()
