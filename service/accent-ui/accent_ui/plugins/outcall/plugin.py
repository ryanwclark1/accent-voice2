# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import OutcallService
from .view import OutcallDestinationView, OutcallView

outcall = create_blueprint('outcall', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        OutcallView.service = OutcallService(clients['accent_confd'])
        OutcallView.register(outcall, route_base='/outcalls')
        register_flaskview(outcall, OutcallView)

        OutcallDestinationView.service = OutcallService(clients['accent_confd'])
        OutcallDestinationView.register(outcall, route_base='/outcall_destination')

        register_listing_url('outcall', 'outcall.OutcallDestinationView:list_json')

        core.register_blueprint(outcall)
