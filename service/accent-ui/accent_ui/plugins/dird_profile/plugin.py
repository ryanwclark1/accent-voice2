# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint

from ..dird_source.service import DirdSourceService
from .service import DirdProfileService
from .view import DirdProfileView

dird_profile = create_blueprint('dird_profile', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        DirdProfileView.service = DirdProfileService(clients['accent_dird'])
        DirdProfileView.source_service = DirdSourceService(clients['accent_dird'])
        DirdProfileView.register(dird_profile, route_base='/dird_profiles')
        register_flaskview(dird_profile, DirdProfileView)

        core.register_blueprint(dird_profile)
