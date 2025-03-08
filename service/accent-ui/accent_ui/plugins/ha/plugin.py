# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from .service import HaService
from .view import HaView

ha = create_blueprint('ha', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        HaView.service = HaService(clients['accent_confd'])
        HaView.register(ha, route_base='/ha')
        register_flaskview(ha, HaView)

        core.register_blueprint(ha)
