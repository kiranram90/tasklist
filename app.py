from flask import Flask
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



@app.route('/test-db')
def test_db():
    try:
        db.session.execute('SELECT 1')  # A simple query to test connection
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"message": str(e)}

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

if __name__ == "__main__":     
    app.run(debug=True)   




