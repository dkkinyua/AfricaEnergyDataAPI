import os
from app.main import app
from dotenv import load_dotenv
from fastapi.testclient import TestClient

load_dotenv()
client = TestClient(app)

# test health endpoint 
def test_health():
    response = client.get("/api/v1/health")
    assert response.json() == {"detail": "API Health OK"}
    assert response.status_code == 200

