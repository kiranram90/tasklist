import pytest
from app import app # Import the Flask app


@pytest.fixture
def client():
    app.testing = True  # Enable testing mode
    return app.test_client()

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