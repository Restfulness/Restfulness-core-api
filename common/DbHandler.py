# NOTE: This class is for handling all calls to database

from common.Link import Link
from common.User import User
from common.Category import Category

from db import db


class DbHandler():
    @staticmethod
    def get_user_object(username: str) -> User:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_id(username: str) -> int:
        user_id = (User.query.
                   with_entities(User.id).filter_by(username=username).first())
        return user_id[0]

    @staticmethod
    def validate_login(username: str, password: str) -> User:
        user = (User.query.filter_by(username=username).first())

        # Check if user exists and password is correct
        if user and user.check_password(password):
            return user
        else:
            return None

    @staticmethod
    def add_new_user(username: str, password: str) -> str:
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if user:
            return "USER_EXISTS"

        user = User(username=username, password_hash=password)
        db.session.add(user)
        db.session.commit()

        return "OK"

    @staticmethod
    def append_new_link(new_link: Link, categories_name: list) -> str:
        """Check if category is already exists or not.
        If category exists, create object. Else create new one
        and then connect new link to categories
        """
        if categories_name:
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
    def remove_link(username: str, link_id: int) -> str:
        link_object = Link.query.filter_by(id=link_id).first()

        # Check if id exists and it's owner sends request
        if link_object:
            if link_object.owner_id == DbHandler.get_user_id(username):
                db.session.delete(link_object)
                db.session.commit()
                return "OK"
            else:
                return "USER_IS_NOT_OWNER"
        else:
            return "ID_NOT_FOUND"

    @staticmethod
    def append_new_categories(link: Link, categories: list) -> str:
        for category in categories:
            category.related_link.append(link)
        db.session.commit()
        return "OK"

    @staticmethod
    def get_links(username: str, link_id: int) -> list:
        user_id = (User.query.
                   with_entities(User.id).filter_by(username=username).first())

        if link_id == -1:
            link_objects = Link.query.filter_by(owner_id=user_id[0]).all()
        else:
            link_objects = Link.query.filter_by(
                owner_id=user_id[0],
                id=link_id
            ).all()

        links_values = [
            {
                "id": link.id,
                "url": link.url,
                "categories": [
                    category.name for category in link.categories
                ]
            }
            for link in link_objects
        ]

        return links_values
