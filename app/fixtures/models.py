from datetime import datetime

from app import db


class Fixture(db.Model):
    __tablename__ = 'main_fixtures'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    install_dt = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return self._repr(name=self.name)
