# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.destination import register_destination_form
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .form import VoicemailDestinationForm
from .service import VoicemailService
from .view import VoicemailDestinationView, VoicemailView

voicemail = create_blueprint('voicemail', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        VoicemailView.service = VoicemailService(clients['accent_confd'])
        VoicemailView.register(voicemail, route_base='/voicemails')
        register_flaskview(voicemail, VoicemailView)

        VoicemailDestinationView.service = VoicemailService(clients['accent_confd'])
        VoicemailDestinationView.register(voicemail, route_base='/voicemails_listing')

        register_destination_form(
            'voicemail', l_('Voicemail'), VoicemailDestinationForm
        )

        register_listing_url(
            'voicemail', 'voicemail.VoicemailDestinationView:list_json'
        )

        core.register_blueprint(voicemail)
