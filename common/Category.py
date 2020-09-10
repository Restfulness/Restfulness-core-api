from db import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))
