# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from .service import ExternalAuthService
from .view import ExternalAuthView

external_auth = create_blueprint('external_auth', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ExternalAuthView.service = ExternalAuthService(clients['accent_auth'])
        ExternalAuthView.register(external_auth, route_base='/external_auths')
        register_flaskview(external_auth, ExternalAuthView)

        core.register_blueprint(external_auth)
