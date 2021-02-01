from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from sqlalchemy.sql import func
import json

with open('config.json', mode='r') as config_file:
    USER_PUBLICITY = json.load(config_file).get(
        'socializing', {}).get('user_publicity_default')


class User(db.Model):
    """
    User model have a one-to-many relationship to Link
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    links = db.relationship('Link', backref='owner',
                            cascade="all, delete-orphan")
    time_created = db.Column(db.DateTime(timezone=True),
                             server_default=func.now())
    time_profile_updated = db.Column(db.DateTime)
    is_public = db.Column(db.Boolean, default=USER_PUBLICITY)
    time_new_link_added = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password_hash = generate_password_hash(self.password_hash)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_password(self, new_password: str):
        self.password_hash = generate_password_hash(new_password)
