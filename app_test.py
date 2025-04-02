import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, Task # Import the Flask app
from models.user import User
from models.task import Task


@pytest.fixture
def test_app():
    # Use the app instance from app.py
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context(): ## app.app_context to emulate a server since 
        db.create_all()  # Create tables
        # Insert initial test data
        db.session.add(Task(title="HW", completed=True))
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    # Use the test client from the app
    return test_app.test_client()


def test_tasks_endpoint(client):
    expected_statuscode = 200
    expected_response_json = {
    "tasks": [
        {
            "completed": True,
            "id": 1,
            "title": "HW"
        }]
    }
    # Send a GET request to the `/hello` endpoint
    response = client.get('/tasks')
    # Assertions
    assert response.status_code == expected_statuscode  # Check the status code
    #assert response.get_json() == expected_response_json  # Check the JSON response

def test_get_task_endpoint(client):
    expected_statuscode = 200
    expected_response_json = {
        "tasks": [
        {
            "completed": True,
            "id": 1,
            "title": "HW"
        }]
    }
    response = client.get('/tasks/1')
    assert response.status_code == expected_statuscode

def test_edit_completed(client):
    expected_completed_value = True
    task_id = 1
    request_body = {"completed":expected_completed_value }
    expected_statuscode = 200
    
    # expected_response_json = {
    #     "tasks" : [
    #         {
    #             "completed": new_val,
    #             "id": task_id,
    #             "title": "HW"
    #         }]
    # }
    # print("This is the expected JSon" ,expected_response_json )
    # print("This is th expected response", expected_response_json )
    response = client.put(f'/tasks/{task_id}', json=request_body)
    assert response.status_code == expected_statuscode
    print("This is the response", response.get_json())
    actual_completed_value = response.get_json()['completed']
    assert actual_completed_value == expected_completed_value

def test_create_task(client):
    expected_statuscode = 200

    request_body = {
        "title":"Swimming class",
        "completed": True
    }

    response = client.post('/tasks', json=request_body)
    assert response.status_code == expected_statuscode 
    print('this is the title', response.get_json()['title'])
    print('this is the title', response.get_json()['completed'])
    assert request_body['title'] == response.get_json()['title']
    assert request_body['completed'] == response.get_json()['completed']

def test_user_model_fields(app_context):
    user = User(username="sampleuser", emiail="sample@example.com")
    user.set_password("testpass")
    db.session.add(user)
    db.session.commit()

    saved_user=User.query.filter_by(username="sampleuser").first()
    assert saved_user.username == "sampleuser"
    assert saved_user.emai == "sample@example.com"
    assert saved_user.password_hash is not None
    assert saved_user.check_password("testpass") is True 


def test_task_model_fields(app_context):
    task = Task(title="Test Task", description=" Task Details", status="completed")
    db.session.add(task)
    db.session.commit()

    saved_task = Task.query.first()
    assert saved_task.title == "Test Task"
    assert saved_task.description == "Task details"
    assert saved_task.status == "pending"


def test_user_task_relationship(app_context):
    user = User(username="taskmaster", email="master@example.com")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()

    task1 = Task(title="Task 1", user_id=user.id)
    task2 = Task(title="Task 2", user_id=user.id)
    db.session.add_all([task1, task2])
    db.session.commit()

    saved_user = User.query.filter_by(username="taskmaster").first()
    assert len(saved_user.tasks) == 2
    task_titles = [task.title for task in saved_user.tasks]
    assert "Task 1" in task_titles
    assert "Task 2" in task_titles


    def test_get_sign_up(client):
        response = client.get('/signup')
        assert response.status_code == 200
        assert b"<form" in response.data

    def test_post_signup_success(client):
        expected_statuscode = 201

        request_body = {
                "username": "newuser",
                "email": "new@example.com",
                "password": "testpass"
            }
        response = client.post('/signup', json=request_body)
        assert response.status_code == expected_statuscode

        response_json = response.get_json()
        print("Signup response:", response_json)
        assert "message" in response_json
        assert response_json["message"] == "User created successfully!"

    def test_post_signup_duplicate_user(client):

        expected_statuscode = 400

         # First signup
        client.post('/signup', json={
        "username": "dupe",
        "email": "dupe@example.com",
        "password": "123"
        })

        # Try again with same data
        response = client.post('/signup', json = {
        "username": "dupe",
        "email": "dupe@example.com",
        "password": "123"
        })

        assert response.status_code == expected_statuscode

        response_json = response.get_json()
        print("Duplicate response:", response_json)

        assert "error" in response_json
        assert response_json["error"] == "Username or email already exists"


    def test_post_signup_missing_fields(client):

        expected_statuscode =400

        request_body = {
            "username": "incomplete"
            # missing email and password
        }

        response = client.post('/signup', json=request_body)
        assert response.status_code == expected_statuscode

        response_json = response.get_json
        print("Missing field response:", response_json)

        assert "error" in response_json
        assert response_json["error"] ==  "All Fields are required"
