# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import (
    ConfigService,
    ConfigurationService,
    PluginService,
    RegistrarService,
)
from .view import (
    ConfigDeviceListingView,
    ConfigDeviceView,
    ConfigRegistrarListingView,
    ConfigRegistrarView,
    ConfigurationView,
    PluginListingView,
    PluginView,
)

provisioning = create_blueprint('provisioning', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PluginView.service = PluginService(clients['accent_provd'])
        PluginView.register(provisioning, route_base='/provisioning/plugins')
        register_flaskview(provisioning, PluginView)

        ConfigRegistrarView.service = RegistrarService(clients['accent_confd'])
        ConfigRegistrarView.register(
            provisioning, route_base='/provisioning/configs/registrar'
        )
        register_flaskview(provisioning, ConfigRegistrarView)

        ConfigRegistrarListingView.service = RegistrarService(clients['accent_confd'])
        ConfigRegistrarListingView.register(
            provisioning, route_base='/config_registrar_listing'
        )
        register_flaskview(provisioning, ConfigRegistrarListingView)

        ConfigDeviceView.service = ConfigService(clients['accent_provd'])
        ConfigDeviceView.register(
            provisioning, route_base='/provisioning/configs/device'
        )
        register_flaskview(provisioning, ConfigDeviceView)

        ConfigDeviceListingView.service = ConfigService(clients['accent_provd'])
        ConfigDeviceListingView.register(
            provisioning, route_base='/config_devices_listing'
        )
        register_flaskview(provisioning, ConfigDeviceListingView)

        PluginListingView.service = PluginService(clients['accent_provd'])
        PluginListingView.register(provisioning, route_base='/plugins_listing')

        register_listing_url('plugin', 'provisioning.PluginListingView:list_json')
        register_listing_url(
            'config_device', 'provisioning.ConfigDeviceListingView:list_json'
        )
        register_listing_url(
            'registrar', 'provisioning.ConfigRegistrarListingView:list_json'
        )

        ConfigurationView.service = ConfigurationService(
            clients['accent_provd'], clients['accent_confd']
        )
        ConfigurationView.register(
            provisioning, route_base='/provisioning/configuration'
        )
        register_flaskview(provisioning, ConfigurationView)

        core.register_blueprint(provisioning)
