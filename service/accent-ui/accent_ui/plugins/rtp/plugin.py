# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from .service import RtpService
from .view import RtpView

rtp = create_blueprint('rtp', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        RtpView.service = RtpService(clients['accent_confd'])
        RtpView.register(rtp, route_base='/rtp')
        register_flaskview(rtp, RtpView)

        core.register_blueprint(rtp)
