from flask import request
from marshmallow import ValidationError

from app import db
from app.utils import base_view
from app.main.models import Subscriber
from ..schemas import SubscriberSchema, AmountArgsSchema


__all__ = ['AddView', 'StatusView', 'SubstractView']


def get_subscriber_and_op_amount(lock=True):
    """
    Функция получающая данные из тела запроса при помощи AmountArgsSchema

    Args:
        lock: нужно ли блокировать строчку с абонентом

    Returns: абонент, сумма операции
    """

    args = AmountArgsSchema().load(request.get_json())
    query = Subscriber.query.filter_by(id=args['id'])
    if lock:
        query = query.with_for_update()

    subscriber = query.first_or_404('subscriber not found')
    if subscriber.is_closed:
        raise ValidationError('subscriber account is closed')

    return subscriber, args['amount']


class AddView(base_view.View):
    """View пополнения счёта абонента"""

    def post(self):
        subscriber, amount = get_subscriber_and_op_amount()
        with db.session_scope():
            subscriber.balance += amount
            return {'balance': subscriber.balance}


class SubstractView(base_view.View):
    """View списания средств со счёта абонента"""

    def post(self):
        subscriber, amount = get_subscriber_and_op_amount()
        with db.session_scope():
            if subscriber.balance < subscriber.hold + amount:
                raise ValidationError('not enough money')

            subscriber.hold += amount
            return {'hold': subscriber.hold}


class StatusView(base_view.View):
    """View получающая данные о счёте абонента"""

    def get(self, pk):
        subscriber = Subscriber.query.get_or_404(pk, 'subscriber not found')
        return SubscriberSchema().dump(subscriber)
