from fastapi.testclient import TestClient

from api.api_main import app

client = TestClient(app)


def test_main_page():
    response = client.get("/")
    assert response.status_code == 200


def test_servers_page():
    response = client.get("/servers")
    assert response.status_code == 200

