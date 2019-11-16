import os

from huey import crontab

from app import app_context
from ..main.models import Subscriber
from . import huey


@huey.periodic_task(
    retries=2,
    retry_delay=60,
    validate_datetime=crontab(minute=f'*/{int(os.getenv("SUBSTRACT_HOLD_PERIOD", "10"))}'),
)
@app_context()
def subtract_holds():
    Subscriber.query.update(
        values={'balance': Subscriber.current_balance, 'hold': 0}, synchronize_session=False
    )
