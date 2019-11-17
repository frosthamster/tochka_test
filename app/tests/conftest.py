import pytest

from app import create_app
from app.configs.config import TestConfig
from app.fixtures import install_fixture


@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    with app.test_request_context():
        yield app


@pytest.fixture(scope='session')
def _db(app, request):
    db = app.extensions['sqlalchemy'].db
    db.create_all()

    @request.addfinalizer
    def clear_db():
        with db.session_scope():
            db.truncate_all_tables()

    with db.session_scope():
        install_fixture('initial')

    return db


@pytest.fixture(autouse=True)
def enable_transactional_tests(db_session):
    pass
