  # Import the Task model and db instance

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  # Single shared instance

from .task import Task
from .user import User
