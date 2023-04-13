from database.database import db


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))


def __init__(self, name):
    self.name = name
