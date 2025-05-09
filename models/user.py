from models import db
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', back_populates='user', cascade="all, delete")

def set_password(self, password):
    self.password_hash = generate_password_hash(password)


def check_password(self, password):
    return check_password_hash(self.password_hash, password)
