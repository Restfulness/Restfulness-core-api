# TODO: This class is just a prototype and it's just for testing puroses

from werkzeug.security import safe_str_cmp

from common.Link import Link
from common.User import User

links = [
    Link("www.stackoverflow.com", ["programming"]),
    Link("www.geeksforgeeks.com", ["programming", "learning"])
]
users = [
    User(1, 'user1', 'zanjan', links[0]),
    User(2, 'test', 'test', links),
]


class DbHandler():
    @staticmethod
    def validate_login(username, password):
        username_table = {u.username: u for u in users}
        user = username_table.get(username, None)

        return_message = ""
        if user and safe_str_cmp(
            user.password.encode('utf-8'), password.encode('utf-8')
        ):
            return_message = user
        else:
            return_message = None

        return return_message

    @staticmethod
    def add_new_user(username, password):
        # Check if user exists
        for user in users:
            if safe_str_cmp(
                user.username.encode('utf-8'), username.encode('utf-8')
            ):
                return 1

        # If user doesn't exist, get Id for it and Signup
        max_id = 0
        for user in users:
            if user.id > max_id:
                max_id = user.id

        # Add new user
        users.append(User(max_id+1, username, password))

        return 0

    @staticmethod
    def get_links(username):
        return_message = ""
        for user in users:
            if user.username == username:
                return_message = user.links

        return return_message
