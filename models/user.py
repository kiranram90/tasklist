from models import db
from sqlalchemy.orm import relationship


class User(db.model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    tasks = db.relationship('Task')