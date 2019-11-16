import logging

from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from .base_view import get_default_resp


logger = logging.getLogger(__name__)


class ExceptionsLoggingFilter:
    def filter(self, record):
        if not record.exc_info:
            return True

        _, exc_value, _ = record.exc_info
        return not isinstance(exc_value, (ValidationError, HTTPException))


def handle_exc(exc):
    logger.exception(f'caught unhandled exception {exc}')
    if isinstance(exc, ValidationError):
        return get_default_resp(None, 400, description=exc.messages)

    if isinstance(exc, HTTPException):
        return get_default_resp(None, exc.code, description=exc.description)

    return get_default_resp(None, 500, description='internal server error')
