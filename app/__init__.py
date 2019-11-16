from dotenv import load_dotenv
from flask_uuid import FlaskUUID

load_dotenv()


from flask import Flask
from flask_migrate import Migrate

import app.utils.logging_config
from .config import Config
from .utils.exceptions import handle_exc
from .utils.sqla_config import get_db


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
