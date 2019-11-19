from marshmallow import fields

from app.utils import base_schema
from ..models import Subscriber

__all__ = ['AmountArgsSchema', 'SubscriberSchema']


class AmountArgsSchema(base_schema.Schema):
    id = fields.UUID(required=True)
    amount = fields.Decimal(2, required=True, validate=lambda e: e > 0)


class SubscriberSchema(base_schema.ModelSchema):
    balance = fields.Decimal(as_string=True)
    hold = fields.Decimal(as_string=True)

    class Meta:
        model = Subscriber
        fields = ('full_name', 'balance', 'hold', 'is_closed')
