from sqlalchemy.dialects.postgresql import UUID

from app import db

__all__ = ['Subscriber']


class Subscriber(db.Model):
    __tablename__ = 'main_subscribers'
    __table_args__ = (
        db.CheckConstraint('balance >= 0', name='balance_gte_0'),
        db.CheckConstraint('hold >= 0', name='hold_gte_0'),
        db.CheckConstraint('hold <= balance', name='hold_lte_balance'),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    hold = db.Column(db.Integer, nullable=False)
    is_closed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return self._repr(full_name=self.full_name, is_closed=self.is_closed)
