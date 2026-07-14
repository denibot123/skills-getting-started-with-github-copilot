import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
            },
            "Gym Class": {
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"],
            },
        }
    )
    yield
    app_module.activities.clear()


def test_duplicate_signup_is_rejected():
    client = TestClient(app_module.app)
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"
    assert app_module.activities[activity_name]["participants"].count(email) == 1
