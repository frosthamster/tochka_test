from flask import url_for


def test_ping(client):
    resp = client.get(url_for('main.ping'))
    assert resp.status_code == 200
    resp = resp.json

    assert resp == {
        'addition': {'msg': "it's alive!"},
        'description': {},
        'result': True,
        'status': 200,
    }
