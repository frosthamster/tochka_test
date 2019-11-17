from flask import Blueprint

bp = Blueprint('main', __name__)

from . import models
from . import urls
