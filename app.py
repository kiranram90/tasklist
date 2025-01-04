from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os # gives access to operating system 
from dotenv import load_dotenv
from alembic import op
from sqlalchemy.sql import text # allows the use of raw SQL using text()
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String


load_dotenv() #loading environment files. Environment configuration files. These you can have access anywhere in the app. 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)  

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route("/kiranvalue")
def home():
    return {'kiran_value_from_env_file': os.getenv('KIRAN')}


@app.route('/tasks', methods=['POST']) #flask decorator instead of using URL pattern
def create_tasks():
    task1 = Task(title="HW", completed = True) #A Task instance (task1) is created with the title "HW" and completed=True.
    db.session.add(task1)  #The task1 instance is added to the SQLAlchemy session (db.session.add(task1)).
    db.session.commit() #The session changes are committed to the database (db.session.commit()), which executes the SQL INSERT statement.
    db.session.refresh(task1) # Ensure task1 remains bound to the session
    return {'task1_title': task1.title}

@app.route('/tasks',methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_list = []
    for task in tasks:
        task_dict = {
            'id': task.id,
            'title' : task.title,
            'completed' : task.completed
        }
        tasks_list.append(task_dict)
    return jsonify({'tasks' : tasks_list}), 200 #proving response code as second return value. It is good practice to wrap return values in jsonify as it fixes format

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task_id(id):
    task = Task.query.get(id) # query.get is outdated in SQLAlchemy so use session
    if not task:
        abort(404, description="Task not Found")
    return jsonify({
            "id" : task.id,
            "title" : task.title,
            "completed" : task.completed
    }), 200



if __name__ == "__main__":     
    app.run(debug=True)   
    





