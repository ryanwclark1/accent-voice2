# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.destination import register_destination_form
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .form import IvrDestinationForm
from .service import IvrService
from .view import IvrDestinationView, IvrView

ivr = create_blueprint('ivr', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        IvrView.service = IvrService(clients['accent_confd'])
        IvrView.register(ivr, route_base='/ivrs')
        register_flaskview(ivr, IvrView)

        IvrDestinationView.service = IvrService(clients['accent_confd'])
        IvrDestinationView.register(ivr, route_base='/ivr_destination')

        register_destination_form('ivr', 'Ivr', IvrDestinationForm)
        register_listing_url('ivr', 'ivr.IvrDestinationView:list_json')

        core.register_blueprint(ivr)
