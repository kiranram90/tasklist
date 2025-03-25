from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.task import Task
from models import db

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        sqla_session = db.session
        load_instance = True