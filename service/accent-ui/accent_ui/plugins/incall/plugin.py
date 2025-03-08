# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from .service import IncallService
from .view import IncallView

incall = create_blueprint('incall', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        IncallView.service = IncallService(clients['accent_confd'])
        IncallView.register(incall, route_base='/incalls')
        register_flaskview(incall, IncallView)

        core.register_blueprint(incall)
