# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from .service import PagingService
from .view import PagingView

paging = create_blueprint('paging', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PagingView.service = PagingService(clients['accent_confd'])
        PagingView.register(paging, route_base='/pagings')
        register_flaskview(paging, PagingView)

        core.register_blueprint(paging)
