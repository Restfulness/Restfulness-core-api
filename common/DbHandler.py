# NOTE: This class is for handling all calls to database

from common.Link import Link
from common.User import User
from common.Category import Category

from db import db


class DbHandler():
    @staticmethod
    def get_user_object(username: str):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def validate_login(username: str, password: str):
        user = User.query.filter_by(username=username).first()

        # Check if user exists and password is correct
        if user and user.check_password(password):
            return user
        else:
            return None

    @staticmethod
    def add_new_user(username: str, password: str):
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if user:
            return "USER_EXISTS"

        user = User(username=username, password_hash=password)
        db.session.add(user)
        db.session.commit()

        return "OK"

    @staticmethod
    def append_new_link(new_link: Link, categories_name: list):
        """Check if category is already exists or not.
        If category exists, create object. Else create new one
        and then connect new link to categories
        """
        for category_name in categories_name:
            category_object = Category.query.filter_by(
                name=category_name
            ).first()
            if not category_object:
                category_object = Category(name=category_name)

            category_object.related_link.append(new_link)

        db.session.add(new_link)
        db.session.commit()
        return "OK"

    @staticmethod
    def remove_link(username: str, link_id: int):
        user_object = User.query.filter_by(username=username).first()
        link_object = Link.query.filter_by(id=link_id).first()

        # Check if id exists and it's owner sends request
        if link_object:
            if link_object.owner_id == user_object.id:
                Link.query.filter_by(id=link_id).delete()
                db.session.commit()
                return "OK"
            else:
                return "USER_IS_NOT_OWNER"
        else:
            return "ID_NOT_FOUND"

    @staticmethod
    def append_new_categories(link: Link, categories: list):
        for category in categories:
            category.related_link.append(link)
        db.session.commit()
        return "OK"
