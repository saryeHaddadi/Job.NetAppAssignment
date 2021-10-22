import pytest

from main import create_app


@pytest.fixture()
def flask_app():
    return create_app()

def test_service_get_run_ids(flask_app):
    pass

