from app.utils import base_view

__all__ = ['PingView']


class PingView(base_view.View):
    """View для отслеживания состояния сервера"""

    def get(self):
        return "it's alive!"
