# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from .service import CallPickupService
from .view import CallPickupView

call_pickup = create_blueprint('call_pickup', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        CallPickupView.service = CallPickupService(clients['accent_confd'])
        CallPickupView.register(call_pickup, route_base='/callpickups')
        register_flaskview(call_pickup, CallPickupView)

        core.register_blueprint(call_pickup)
