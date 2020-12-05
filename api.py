from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import json

from resources.user.Login import Login
from resources.user.Signup import Signup
from resources.user.password.ForgetPassword import ForgetPassword
from resources.user.password.VerifyCode import VerifyCode
from resources.user.password.ResetPassword import ResetPassword
from resources.user.Publicity import Publicity
from resources.user.Socializing.Activity import Activity

from resources.links.LinksDeleter import LinksDeleter
from resources.links.LinksAdder import LinksAdder
from resources.links.LinksGetter import LinksGetter
from resources.categories.CategoriesGetter import CategoriesGetter
from resources.links.LinksGetterByCategory import LinksGetterByCategory
from resources.links.LinksGetterBySearch import LinksGetterBySearch
from resources.links.LinksUpdateCategory import LinksUpdateCategory


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
if CONFIG.get('database', {}).get('mysql'):
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
    LinksGetter,
    CONFIG.get('routes', {}).get('links', {}).get('main'),
    CONFIG.get('routes', {}).get('links', {}).get('get_id'),
    endpoint='links'
)
api.add_resource(
    LinksDeleter,
    CONFIG.get('routes', {}).get('links', {}).get('get_id')
)
api.add_resource(
    LinksAdder,
    CONFIG.get('routes', {}).get('links', {}).get('main')
)
api.add_resource(
    CategoriesGetter,
    CONFIG.get('routes', {}).get('categories', {}).get('main'),
    CONFIG.get('routes', {}).get('categories', {}).get('get_id'),
    endpoint='categories'
)
api.add_resource(
    LinksGetterByCategory,
    CONFIG.get('routes', {}).get('links', {}).get('by_category_id'),
)
api.add_resource(
    LinksGetterBySearch,
    CONFIG.get('routes', {}).get('links', {}).get('by_pattern_string')
)
api.add_resource(
    ForgetPassword,
    CONFIG.get('routes', {}).get('user', {}).get('forget_password')
)
api.add_resource(
    VerifyCode,
    CONFIG.get('routes', {}).get('user', {}).get('verify_code')
)
api.add_resource(
    ResetPassword,
    CONFIG.get('routes', {}).get('user', {}).get('reset_password')
)
api.add_resource(
    LinksUpdateCategory,
    CONFIG.get('routes', {}).get('links', {}).get('update_category')
)
api.add_resource(
    Publicity,
    CONFIG.get('routes', {}).get('user', {}).get('publicity')
)
api.add_resource(
    Activity,
    CONFIG.get('routes', {}).get('user', {}).get('activity_list')
)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(host=CONFIG.get('host'))
