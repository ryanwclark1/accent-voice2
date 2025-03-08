# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from .service import DhcpService
from .view import DhcpView

dhcp = create_blueprint('dhcp', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        DhcpView.service = DhcpService(clients['accent_confd'])
        DhcpView.register(dhcp, route_base='/dhcp')
        register_flaskview(dhcp, DhcpView)

        core.register_blueprint(dhcp)
