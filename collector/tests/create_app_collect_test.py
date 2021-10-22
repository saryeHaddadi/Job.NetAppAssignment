import pytest

from main import create_app


@pytest.fixture()
def flask_app():
    return create_app()

def can_collect_payloads(flask_app):
    pass
    # with flask_app.test_client() as client:
    #     response = client.get("/collect") # POST
    #     assert response.status_code == 200

