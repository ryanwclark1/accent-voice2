# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from .service import HepService
from .view import HepView

hep = create_blueprint('hep', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        HepView.service = HepService(clients['accent_confd'])
        HepView.register(hep, route_base='/hep')
        register_flaskview(hep, HepView)

        core.register_blueprint(hep)
