import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, Task # Import the Flask app


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
