from db import db
from common.Relationships import links_to_categories
from sqlalchemy.sql import func


class Link(db.Model):
    """
    Link model has a one-to-many relationship to User
    and a many-to-many relationship to Category
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(350))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    categories = db.relationship(
        'Category',
        secondary=links_to_categories,
        backref=db.backref(
            'related_link',
            lazy='dynamic',
        )
    )
    time_created = db.Column(db.DateTime(timezone=True),
                             server_default=func.now())
