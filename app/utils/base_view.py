import collections.abc

from flask import current_app, jsonify
from flask.views import MethodView


def to_dict(obj):
    if obj is None:
        return {}

    if isinstance(obj, collections.abc.Mapping):
        return obj

    return {'msg': obj}


def get_default_resp(result, status=200, description=None):
    resp = {
        'status': status,
        'result': 200 <= status < 300,
        'addition': to_dict(result),
        'description': to_dict(description),
    }

    return jsonify(resp), status


class Response:
    def __init__(self, result, **kwargs):
        self.result = result
        self.additional_kwargs = kwargs


class View(MethodView):
    def dispatch_request(self, *args, **kwargs):
        resp = super().dispatch_request(*args, **kwargs)
        status = 200
        description = {}

        if isinstance(resp, current_app.response_class):
            return resp

        if isinstance(resp, tuple):
            if len(resp) != 2:
                raise ValueError('expected (resp, code) syntax')

            if isinstance(resp[0], current_app.response_class):
                return resp

            resp, status = resp

        if isinstance(resp, Response):
            description = resp.additional_kwargs
            resp = resp.result

        return get_default_resp(result=resp, status=status, description=description)
