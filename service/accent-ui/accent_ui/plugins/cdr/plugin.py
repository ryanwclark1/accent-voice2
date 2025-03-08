# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from .service import CdrService
from .view import CdrView

cdr = create_blueprint('cdr', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        CdrView.service = CdrService(clients['accent_call_logd'])
        CdrView.register(cdr, route_base='/cdrs')
        register_flaskview(cdr, CdrView)

        core.register_blueprint(cdr)
