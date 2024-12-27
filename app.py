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

@app.route("/kiranvalue")
def home():
    return {'kiran_value_from_env_file': os.getenv('KIRAN')}

if __name__ == "__main__":     
    app.run(debug=True)   
