from pathlib import Path
import sys

from fastapi.testclient import TestClient


sys.path.insert(
    0,
    str(
        Path(__file__)
        .resolve()
        .parents[1]
    )
)


from main import app


client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_validation():

    response = client.post(
        "/qa",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422