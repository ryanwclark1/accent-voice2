# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import TrunkService
from .view import TrunkListingView, TrunkView

trunk = create_blueprint('trunk', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        TrunkView.service = TrunkService(clients['accent_confd'])
        TrunkView.register(trunk, route_base='/trunks')
        register_flaskview(trunk, TrunkView)

        TrunkListingView.service = TrunkService(clients['accent_confd'])
        TrunkListingView.register(trunk, route_base='/trunks_listing')

        register_listing_url('trunk', 'trunk.TrunkListingView:list_json')

        core.register_blueprint(trunk)
