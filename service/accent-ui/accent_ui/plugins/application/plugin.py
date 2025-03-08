# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.core.form import register_destination_form_application
from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .form import (
    ApplicationCustomDestination,
    NodeDestinationForm,
    NoneDestinationForm,
    register_application_destination_form,
)
from .service import ApplicationService
from .view import ApplicationDestinationView, ApplicationView

application = create_blueprint('application', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ApplicationView.service = ApplicationService(clients['accent_confd'])
        ApplicationView.register(application, route_base='/applications')
        register_flaskview(application, ApplicationView)

        ApplicationDestinationView.service = ApplicationService(clients['accent_confd'])
        ApplicationDestinationView.register(
            application, route_base='/applications_listing'
        )
        register_destination_form_application(
            'custom', l_('Custom'), ApplicationCustomDestination
        )

        register_application_destination_form(
            'None', l_('None'), NoneDestinationForm, position=0
        )
        register_application_destination_form('node', l_('Node'), NodeDestinationForm)

        # TODO: should register to something like application:custom, not only custom
        # But that would add another layer of logic in the template ...
        register_listing_url(
            'custom', 'application.ApplicationDestinationView:list_json'
        )

        core.register_blueprint(application)
