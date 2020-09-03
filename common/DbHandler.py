# NOTE: This class is for handling all calls to database

from common.Link import Link
from common.User import User

from db import db


class DbHandler():
    @staticmethod
    def get_user_object(username: str):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def validate_login(username: str, password: str):
        user = User.query.filter_by(username=username).first()

        # Chech if user exists and password is correct
        if user and user.check_password(password):
            return user
        else:
            return None

    @staticmethod
    def add_new_user(username: str, password: str):
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if user:
            return 1

        user = User(username=username, password_hash=password)
        db.session.add(user)
        db.session.commit()

        return 0

    @staticmethod
    def append_new_link(new_link: Link):
        db.session.add(new_link)
        db.session.commit()
        return 0

    @staticmethod
    def remove_link(username: str, link_id: int):
        user_object = User.query.filter_by(username=username).first()
        link_object = Link.query.filter_by(id=link_id).first()

        # Check if id exists and it's owner sends request
        if link_object:
            if link_object.owner_id == user_object.id:
                Link.query.filter_by(id=link_id).delete()
                db.session.commit()
                return 0
            else:
                return 1
        else:
            return 2
