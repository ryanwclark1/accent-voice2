# Copyright 2023 Accent Communications

from flask_babel import lazy_gettext as l_

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.destination import register_destination_form
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .form import ExtensionDestinationForm
from .service import ExtensionFeaturesService, ExtensionService
from .view import ExtensionFeaturesView, ExtensionListingView, ExtensionView

extension = create_blueprint('extension', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        ExtensionView.service = ExtensionService(clients['accent_confd'])
        ExtensionView.register(extension, route_base='/extensions')
        register_flaskview(extension, ExtensionView)

        ExtensionFeaturesView.service = ExtensionFeaturesService(clients['accent_confd'])
        ExtensionFeaturesView.register(extension, route_base='/extensions_features')
        register_flaskview(extension, ExtensionFeaturesView)

        ExtensionListingView.service = ExtensionService(clients['accent_confd'])
        ExtensionListingView.register(extension, route_base='/extensions_listing')

        register_destination_form(
            'extension', l_('Extension'), ExtensionDestinationForm
        )

        register_listing_url(
            'available_extension_incall',
            'extension.ExtensionListingView:list_available_exten_incall',
        )
        register_listing_url(
            'available_extension_group',
            'extension.ExtensionListingView:list_available_exten_group',
        )
        register_listing_url(
            'available_extension_user',
            'extension.ExtensionListingView:list_available_exten_user',
        )
        register_listing_url(
            'available_extension_queue',
            'extension.ExtensionListingView:list_available_exten_queue',
        )
        register_listing_url(
            'available_extension_conference',
            'extension.ExtensionListingView:list_available_exten_conference',
        )

        core.register_blueprint(extension)
