import pytest

from . import create_app
from .configs.config import TestConfig
from .fixtures import install_fixture


@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    with app.test_request_context():
        yield app


@pytest.fixture(scope='session')
def _db(app, pytestconfig):
    db = app.extensions['sqlalchemy'].db

    if pytestconfig.getoption('--create-db'):
        with db.session_scope():
            db.drop_all()
            db.create_all()
            install_fixture(pytestconfig.getoption('--fixture-name'))

    return db


@pytest.fixture(autouse=True)
def enable_transactional_tests(db_session):
    pass
