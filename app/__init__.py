from dotenv import load_dotenv

load_dotenv()

from contextlib import ExitStack, contextmanager

from flask import Flask
from flask_uuid import FlaskUUID
from flask_migrate import Migrate

from .configs.config import Config
from .configs.sqla_config import get_db
from .utils.exceptions import handle_exc


db = get_db()
migrate = Migrate()
flask_uuid = FlaskUUID()


def create_app(app_config=Config):
    app = Flask(__name__)
    app.config.from_object(app_config)

    db.init_app(app)
    migrate.init_app(app, db)
    flask_uuid.init_app(app)

    from .main import bp as main_bp

    app.register_blueprint(main_bp, url_prefix='/api/')

    app.register_error_handler(Exception, handle_exc)

    return app


@contextmanager
def app_context(use_db=True, *args, **kwargs):
    """
    Декоратор/контекстный менеджер, поднимающий контекст приложения

    Args:
        use_db: нужно ли создавать сессию бд в скоупе
        *args: аргументы для создания сессии
        **kwargs:

    Returns: созданная сессия
    """
    app = create_app()
    with ExitStack() as stack:
        session = None
        stack.enter_context(app.test_request_context())
        if use_db:
            session = stack.enter_context(db.session_scope(remove=True, *args, **kwargs))

        yield session
