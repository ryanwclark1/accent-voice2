# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.destination import register_destination_form
from accent_ui.helpers.funckey import register_funckey_destination_form
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .form import ConferenceDestinationForm, ConferenceFuncKeyDestinationForm
from .service import ConferenceService
from .view import ConferenceDestinationView, ConferenceView

conference = create_blueprint('conference', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ConferenceView.service = ConferenceService(clients['accent_confd'])
        ConferenceView.register(conference, route_base='/conferences')
        register_flaskview(conference, ConferenceView)

        ConferenceDestinationView.service = ConferenceService(clients['accent_confd'])
        ConferenceDestinationView.register(
            conference, route_base='/conference_destination'
        )

        register_destination_form(
            'conference', l_('Conference'), ConferenceDestinationForm
        )
        register_funckey_destination_form(
            'conference', l_('Conference'), ConferenceFuncKeyDestinationForm
        )
        register_listing_url(
            'conference', 'conference.ConferenceDestinationView:list_json'
        )

        core.register_blueprint(conference)
