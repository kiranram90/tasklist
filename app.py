from flask import Flask,request, jsonify, abort
from models import db
from flask_migrate import Migrate
import os # gives access to operating system 
from dotenv import load_dotenv
from alembic import op
from sqlalchemy.sql import text # allows the use of raw SQL using text()
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from models import Task, db



load_dotenv() #loading environment files. Environment configuration files. These you can have access anywhere in the app. 

app = Flask(__name__)



class Config():
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Testconfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5436/test-todo'
    
db.init_app(app)

migrate = Migrate(app, db)  


@app.route("/kiranvalue")
def home():
    return {'kiran_value_from_env_file': os.getenv('KIRAN')}


# @app.route('/tasks', methods=['POST']) #flask decorator instead of using URL pattern
# def create_tasks():
#     task1 = Task(title="HW", completed = True) #A Task instance (task1) is created with the title "HW" and completed=True.
#     db.session.add(task1)  #The task1 instance is added to the SQLAlchemy session (db.session.add(task1)).
#     db.session.commit() #The session changes are committed to the database (db.session.commit()), which executes the SQL INSERT statement.
#     db.session.refresh(task1) # Ensure task1 remains bound to the session
#     return {'task1_title': task1.title}

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

@app.route('/tasks/<int:id>', methods=['PUT'])
def edit_completed(id):
    task = Task.query.get(id) 
    if not task:
        abort(404, description="Task not Found")

    data = request.get_json()
    if not data or 'completed' not in data:
        abort (400, description="Request Body must contain 'completed field")

    new_val = data['completed'] # getting new val from the body of the request
    
    if type(new_val) is not bool:
        abort(400, description="'Completed' field must be true/false")

    task.completed = new_val #updating task completed to new val in the server
    # db.session.commit() #saving changes in the server

    return jsonify({
            "id" : task.id,
            "title" : task.title,
            "completed" : task.completed
    }), 200
    

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    print(data)
    if not 'completed' or 'title' not in data:
        abort(400, description = "Please enter all required data")

    stripped_title = data['title'].strip()
    if len(stripped_title) <= 1 or stripped_title == " ": 
        abort(400, description = "Title cannot be empty or less than 1 character" )
    else: new_title = data['title']
    new_completed = data['completed']

    if type(new_completed) is not bool:
        abort(400, description = " Completed needs to be true or false")

    task = Task(title = new_title, completed = new_completed)
    db.session.add(task)  #The task1 instance is added to the SQLAlchemy session (db.session.add(task1)).
    db.session.commit() #The session changes are committed to the database (db.session.commit()), which executes the SQL INSERT statement.
    db.session.refresh(task)

    return jsonify({
        "id" : task.id,
        "title" :task.title, 
        "completed" : task.completed
    }), 200

# @app.route('tasks/<int:id>', methods=['DELETE'])
# def delete_task(id):
#     task = Task.query.get(id)
#     if not task:
#         abort(400, description="Task Not found")
#     db.session.delete(task)
#     db.session.commit()
#     db.session.refresh(task)
#     return {"message": "Task Deleted"}, 200
    

    
    
    

    





if __name__ == "__main__":     
    app.run(debug=True)   
    





