# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import TransportService
from .view import TransportDestinationView, TransportView

transport = create_blueprint('transports', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        TransportView.service = TransportService(clients['accent_confd'])
        TransportView.register(transport, route_base='/transports')
        register_flaskview(transport, TransportView)

        TransportDestinationView.service = TransportService(clients['accent_confd'])
        TransportDestinationView.register(transport, route_base='/transports_listing')

        register_listing_url(
            'transport', 'transports.TransportDestinationView:list_json'
        )

        core.register_blueprint(transport)
