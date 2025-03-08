# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.destination import register_destination_form
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .form import SoundDestinationForm
from .service import SoundService
from .view import SoundFileView, SoundListingView, SoundView

sound = create_blueprint('sound', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        SoundView.service = SoundService(clients['accent_confd'])
        SoundView.register(sound, route_base='/sound')
        register_flaskview(sound, SoundView)

        SoundFileView.service = SoundService(clients['accent_confd'])
        SoundFileView.register(sound, route_base='/sound_files')
        register_flaskview(sound, SoundFileView)

        SoundListingView.service = SoundService(clients['accent_confd'])
        SoundListingView.register(sound, route_base='/sound_listing')

        register_destination_form('sound', l_('Sound'), SoundDestinationForm)

        register_listing_url('sound', 'sound.SoundListingView:list_json')

        core.register_blueprint(sound)
