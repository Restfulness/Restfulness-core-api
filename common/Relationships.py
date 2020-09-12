"""
This file is for showing many-to-many relationships between models.
"""

from db import db


links_to_categories = db.Table(
    'links_to_categories',
    db.Column('link_id', db.Integer, db.ForeignKey('link.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                               )
