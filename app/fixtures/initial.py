from app import db
from . import fixture
from ..main.models import Subscriber


@fixture
@db.session_scope(remove=True)
def run():
    db.session.add_all(
        [
            Subscriber(
                id='26c940a1-7228-4ea2-a3bce6460b172040',
                full_name='Петров Иван Сергеевич',
                balance=1700,
                hold=300,
                is_closed=False,
            ),
            Subscriber(
                id='7badc8f8-65bc-449a-8cde855234ac63e1',
                full_name='Kazitsky Jason',
                balance=200,
                hold=200,
                is_closed=False,
            ),
            Subscriber(
                id='867f0924-a917-4711-939b90b179a96392',
                full_name='Петечкин Петр Измаилович',
                balance=1_000_000,
                hold=1,
                is_closed=True,
            ),
        ]
    )
