from flask import Flask,request, jsonify, abort
from models import db
from flask_migrate import Migrate
import os # gives access to operating system 
from dotenv import load_dotenv
from alembic import op
from sqlalchemy.sql import text # allows the use of raw SQL using text()
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from models.task import Task, TaskSchema
from routes import tasks_bp

task_schema = TaskSchema() ## task_schema (single schema) when dealing with a single task (like GET /tasks/<id> or POST /tasks response).
tasks_schema = TaskSchema(many=True) ##when dealing with a list of tasks.



load_dotenv() #loading environment files. Environment configuration files. These you can have access anywhere in the app. 

app = Flask(__name__)
app.register_blueprint(tasks_bp) # Register the blueprint with the app


class Config():
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Testconfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5436/test-todo'
    
db.init_app(app)

migrate = Migrate(app, db)  




if __name__ == "__main__":     
    app.run(debug=True)   
    





