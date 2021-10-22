import pytest

from main import create_app


@pytest.fixture()
def flask_app():
    return create_app()

def test_service_duration(flask_app):
    pass
    # with flask_app.test_client() as client:
    #     response = client.get("/get_duration") # set a path
    #     assert response.status_code == 200

