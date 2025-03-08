# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import EndpointSIPTemplateService
from .view import EndpointSIPTemplateView, SIPTemplateDestinationView

sip_template = create_blueprint('sip_template', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        EndpointSIPTemplateView.service = EndpointSIPTemplateService(
            clients['accent_confd']
        )
        EndpointSIPTemplateView.register(sip_template, route_base='/sip_templates')
        register_flaskview(sip_template, EndpointSIPTemplateView)

        SIPTemplateDestinationView.service = EndpointSIPTemplateService(
            clients['accent_confd']
        )
        SIPTemplateDestinationView.register(
            sip_template, route_base='/sip_templates_listing'
        )

        register_listing_url(
            'sip_template', 'sip_template.SIPTemplateDestinationView:list_json'
        )

        core.register_blueprint(sip_template)
