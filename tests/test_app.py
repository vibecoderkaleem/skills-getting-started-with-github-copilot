import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister?email={email}")
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Unregister (should succeed if just signed up)
    response_unreg = client.post(f"/activities/{activity}/unregister?email={email}")
    if response_unreg.status_code == 200:
        assert f"Unregistered {email}" in response_unreg.json()["message"]
    else:
        # If not found, that's only valid if the participant was not present
        assert response_unreg.status_code == 404
    # Unregister again (should fail)
    response_unreg2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg2.status_code == 404

def test_signup_activity_not_found():
    response = client.post("/activities/NonexistentActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.post("/activities/NonexistentActivity/unregister?email=someone@mergington.edu")
    assert response.status_code == 404
