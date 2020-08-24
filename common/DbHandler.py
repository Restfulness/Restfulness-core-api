# NOTE: This class is just a prototype and it's just for testing purposes

from werkzeug.security import safe_str_cmp

from common.Link import Link
from common.User import User

links = [
    Link("www.stackoverflow.com", ["programming"]),
    Link("www.geeksforgeeks.com", ["programming", "learning"])
]

USERS = {
    'user1': User(1, 'user1', 'zanjan', links[0]),
    'test': User(2, 'test', 'test', links)
}


class DbHandler():
    @staticmethod
    def validate_login(username: str, password: str):
        user = USERS.get(username)

        return_message = ""
        if user and safe_str_cmp(
            user.password.encode('utf-8'), password.encode('utf-8')
        ):
            return_message = user
        else:
            return_message = None

        return return_message

    @staticmethod
    def add_new_user(username: str, password: str):
        # Check if user exists
        if username in USERS:
            return 1

        # If user doesn't exist, get Id for it and Signup
        max_id = 0
        for user in USERS.values():
            if user.id > max_id:
                max_id = user.id

        # Add new user
        USERS[username] = User(max_id+1, username, password)

        return 0

    @staticmethod
    def get_links(username: str):
        return USERS.get(username).links

    @staticmethod
    def append_new_link(username: str, new_link: Link):
        USERS[username].append_new_link(new_link)
        return 0
