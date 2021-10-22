import pytest

from main import create_app


@pytest.fixture()
def flask_app():
    return create_app()

def test_service_is_healthy(flask_app):
    with flask_app.test_client() as client:
        response = client.get("/health")
        assert response.status_code == 200

