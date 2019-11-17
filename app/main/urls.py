from . import bp

from .views import PingView, AddView, SubstractView, StatusView

bp.add_url_rule('/ping', view_func=PingView.as_view('ping'))
bp.add_url_rule('/add', view_func=AddView.as_view('subscriber_add'))
bp.add_url_rule('/substract', view_func=SubstractView.as_view('subscriber_substract'))
bp.add_url_rule('/status/<uuid:pk>', view_func=StatusView.as_view('subscriber_status'))
