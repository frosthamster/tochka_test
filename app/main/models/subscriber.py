from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from app import db

__all__ = ['Subscriber']


class Subscriber(db.Model):
    """
    Модель абонента

    Attributes:
        full_name: ФИО абонента
        balance: текущий баланс абонента
        hold: зарезервированные средства на счете, подлежащие списанию
        is_closed: закрыт ли счёт
    """

    __tablename__ = 'main_subscribers'
    __table_args__ = (
        db.CheckConstraint('balance >= 0', name='balance_gte_0'),
        db.CheckConstraint('hold >= 0', name='hold_gte_0'),
        db.CheckConstraint('hold <= balance', name='hold_lte_balance'),
    )

    id = db.Column(
        UUID(as_uuid=True), server_default=db.text('uuid_generate_v4()'), primary_key=True
    )
    full_name = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Numeric(precision=64, scale=2), nullable=False)
    hold = db.Column(db.Numeric(precision=64, scale=2), nullable=False)
    is_closed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return self._repr(full_name=self.full_name, is_closed=self.is_closed)

    @hybrid_property
    def current_balance(self):
        return self.balance - self.hold
