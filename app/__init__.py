from dotenv import load_dotenv

load_dotenv()


from flask import Flask
from flask_migrate import Migrate

from .config import Config
from .utils.exceptions import handle_exc
from .utils.sqla_config import get_db


db = get_db()
migrate = Migrate()


def create_app(app_config=Config):
    app = Flask(__name__)
    app.config.from_object(app_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .main import bp as main_bp

    app.register_blueprint(main_bp)

    app.register_error_handler(Exception, handle_exc)

    return app
