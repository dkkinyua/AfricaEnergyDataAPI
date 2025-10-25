import os
from app.main import app
from dotenv import load_dotenv
from fastapi.testclient import TestClient

load_dotenv()
client = TestClient(app)

# test test endpoint
def test_validation_endpoint():
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-key": os.getenv("DEMO_KEY_1")
    }

    response = client.get("/api/v1/test", headers=headers)
    assert response.json() == {"detail": "API Key OK"}
    assert response.status_code == 200

# test health endpoint 
def test_health():
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-key": os.getenv("DEMO_KEY_1")
    }
    response = client.get("/api/v1/health", headers=headers)
    assert response.json() == {"detail": "API Health OK"}
    assert response.status_code == 200

