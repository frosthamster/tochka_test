from flask import Blueprint

bp = Blueprint('main', __name__)

from . import models  # noqa isort:skip
from . import urls  # noqa isort:skip
