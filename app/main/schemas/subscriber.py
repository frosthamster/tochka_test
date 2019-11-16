from marshmallow import fields

from app.utils import base_schema
from ..models import Subscriber

__all__ = ['AmountArgsSchema', 'SubscriberSchema']


class AmountArgsSchema(base_schema.Schema):
    id = fields.UUID(required=True)
    amount = fields.Decimal(2, required=True, validate=lambda e: e > 0)


class SubscriberSchema(base_schema.ModelSchema):
    class Meta:
        model = Subscriber
        fields = ('balance', 'hold', 'is_closed')
