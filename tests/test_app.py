import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def client():
    app_module.activities = app_module.create_activities()
    return TestClient(app_module.app)


def test_duplicate_signup_is_rejected(client):
    response = client.post("/activities/Chess Club/signup?email=teststudent@mergington.edu")
    assert response.status_code == 200

    response = client.post("/activities/Chess Club/signup?email=teststudent@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_from_activity(client):
    response = client.post("/activities/Chess Club/signup?email=teststudent@mergington.edu")
    assert response.status_code == 200

    response = client.delete("/activities/Chess Club/unregister?email=teststudent@mergington.edu")
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered teststudent@mergington.edu from Chess Club"

    activity = client.get("/activities").json()["Chess Club"]
    assert "teststudent@mergington.edu" not in activity["participants"]


def test_unregister_missing_participant_returns_404(client):
    response = client.delete("/activities/Chess Club/unregister?email=missing@mergington.edu")
    assert response.status_code == 404
