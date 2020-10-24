from db import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))

    # Below methods are for adding Category objects to a set variable
    def __hash__(self):
        return(hash(self.id))

    def __eq__(self, next_category):
        return(True if self.id == next_category.id else False)
