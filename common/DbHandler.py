# NOTE: This class is just a prototype and it's just for testing purposes

from common.Link import Link
from common.User import User

from db import db

links = [
    Link("www.stackoverflow.com", ["programming"]),
    Link("www.geeksforgeeks.com", ["programming", "learning"])
]


class DbHandler():
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
    def get_links(username: str):
        # return USERS.get(username).links
        return 0

    @staticmethod
    def append_new_link(username: str, new_link: Link):
        # USERS[username].append_new_link(new_link)
        return 0

    @staticmethod
    def remove_link(username: str, address_name: str):
        """link_found_status = False

        for (index, link) in enumerate(USERS[username].get_links()):
            if link.get_address_name() == address_name:
                link_found_status = True
                del(USERS[username].get_links()[index])
                break

        if link_found_status:
            return 0
        else:
            return 1"""
        return 0
