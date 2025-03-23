from models import db
from sqlalchemy.orm import relationship
from marshmallow import Schema,fields,validate, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        sqla_session = db.session 
        load_instance = True  # So it can load data into SQLAlchemy models if needed