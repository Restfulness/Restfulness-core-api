from werkzeug.security import generate_password_hash, check_password_hash
from db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password_hash = generate_password_hash(self.password_hash)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


"""
class User():
    def __init__(self, user_id, username, password, links=""):
        self.id = user_id
        self.username = username
        self.password = password
        # Make sure that input is a list
        if isinstance(links, list):
            self.links = links
        else:
            self.links = [links]

    def get_links(self):
        return self.links

    def append_new_link(self, link):
        self.links.append(link)

    def __repr__(self):
        return f"User(id='{self.id}')"

    def __str__(self):
        return f"User(id='{self.id}')"
"""
