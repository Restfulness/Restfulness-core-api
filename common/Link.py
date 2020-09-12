from db import db
from common.Relationships import links_to_categories


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(50))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    categories = db.relationship(
        'Category',
        secondary=links_to_categories,
        backref=db.backref(
            'related_link',
            lazy='dynamic'
        )
    )
