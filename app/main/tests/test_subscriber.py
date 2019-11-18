from uuid import UUID

import pytest
from flask import url_for

from app.message_queue.huey_tasks import subtract_holds
from ..models import Subscriber


@pytest.fixture
def active_subscriber():
    return Subscriber.query.get('26c940a1-7228-4ea2-a3bce6460b172040')


@pytest.fixture
def inactive_subscriber():
    return Subscriber.query.get('867f0924-a917-4711-939b90b179a96392')


@pytest.fixture
def invalid_pk():
    return UUID('00000000-0000-0000-0000000000000000')


def test_status(client, active_subscriber):
    resp = client.get(url_for('main.subscriber_status', pk=active_subscriber.id))
    assert resp.status_code == 200
    resp = resp.json

    assert resp == {
        'addition': {
            'balance': active_subscriber.balance,
            'hold': active_subscriber.hold,
            'is_closed': active_subscriber.is_closed,
        },
        'description': {},
        'result': True,
        'status': 200,
    }


def test_fail_status_invalid_pk(client, invalid_pk):
    resp = client.get(url_for('main.subscriber_status', pk=invalid_pk))
    assert resp.status_code == 404


def test_add(client, active_subscriber, db_session):
    old_balance = active_subscriber.balance
    resp = client.post(
        url_for('main.subscriber_add'), json={'id': active_subscriber.id, 'amount': '300'}
    )
    assert resp.status_code == 200
    resp = resp.json

    db_session.expire(active_subscriber)
    assert old_balance + 300 == active_subscriber.balance

    assert resp == {
        'addition': {'balance': active_subscriber.balance},
        'description': {},
        'result': True,
        'status': 200,
    }


def test_fail_add_invalid_pk(client, invalid_pk):
    resp = client.post(url_for('main.subscriber_add'), json={'id': invalid_pk, 'amount': '300'})
    assert resp.status_code == 404


def test_fail_add_on_inactive(client, inactive_subscriber):
    resp = client.post(
        url_for('main.subscriber_add'), json={'id': inactive_subscriber.id, 'amount': '300'}
    )
    assert resp.status_code == 400


def test_fail_add_missing_data(client):
    resp = client.post(url_for('main.subscriber_add'), json={})
    assert resp.status_code == 400


def test_substract(client, active_subscriber, db_session):
    old_hold = active_subscriber.hold
    resp = client.post(
        url_for('main.subscriber_substract'), json={'id': active_subscriber.id, 'amount': '100'}
    )
    assert resp.status_code == 200
    resp = resp.json

    db_session.expire(active_subscriber)
    assert old_hold + 100 == active_subscriber.hold

    assert resp == {
        'addition': {'hold': active_subscriber.hold},
        'description': {},
        'result': True,
        'status': 200,
    }


def test_fail_substract_invalid_pk(client, invalid_pk):
    resp = client.post(
        url_for('main.subscriber_substract'), json={'id': invalid_pk, 'amount': '100'}
    )
    assert resp.status_code == 404


def test_fail_substract_on_inactive(client, inactive_subscriber):
    resp = client.post(
        url_for('main.subscriber_substract'), json={'id': inactive_subscriber.id, 'amount': '100'}
    )
    assert resp.status_code == 400


def test_fail_substract_too_big(client, active_subscriber):
    resp = client.post(
        url_for('main.subscriber_substract'), json={'id': active_subscriber.id, 'amount': '1401'}
    )
    assert resp.status_code == 400


def test_fail_substract_missing_data(client):
    resp = client.post(url_for('main.subscriber_substract'), json={})
    assert resp.status_code == 400


def test_substract_hold(active_subscriber, db_session):
    old_balance, old_hold = active_subscriber.balance, active_subscriber.hold
    db_session.expire(active_subscriber)
    subtract_holds.call_local()

    assert active_subscriber.hold == 0
    assert active_subscriber.balance == old_balance - old_hold
