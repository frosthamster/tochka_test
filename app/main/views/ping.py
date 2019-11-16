from app.utils import base_view

__all__ = ['PingView']


class PingView(base_view.View):
    def get(self):
        return "it's alive!"
