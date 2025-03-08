# Copyright 2023 Accent Communications

from accent_ui.flask_menu.classy import register_flaskview
from accent_ui.helpers.plugin import create_blueprint
from accent_ui.helpers.view import register_listing_url

from .service import (
    ConfBridgeGeneralSettingsService,
    FeaturesGeneralSettingsService,
    IaxGeneralSettingsService,
    PJSIPDocService,
    PJSIPGlobalSettingsService,
    PJSIPSystemSettingsService,
    SCCPDocService,
    SCCPGeneralSettingsService,
    TimezoneService,
    VoicemailGeneralSettingsService,
)
from .view import (
    ConfBridgeGeneralSettingsView,
    FeaturesGeneralSettingsView,
    IaxGeneralSettingsView,
    PJSIPDocListingView,
    PJSIPGlobalSettingsView,
    PJSIPSystemSettingsView,
    SCCPDocListingView,
    SCCPGeneralSettingsView,
    TimezoneListingView,
    VoicemailGeneralSettingsView,
)

general_settings = create_blueprint('general_settings', __name__)


class Plugin:
    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        PJSIPDocListingView.service = PJSIPDocService(clients['accent_confd'])
        PJSIPDocListingView.register(
            general_settings, route_base='/list_json_by_section'
        )
        register_listing_url(
            'pjsip_doc', 'general_settings.PJSIPDocListingView:list_json_by_section'
        )

        SCCPDocListingView.service = SCCPDocService()
        SCCPDocListingView.register(general_settings, route_base='/sccp_documentation')
        register_listing_url(
            'sccp_doc', 'general_settings.SCCPDocListingView:list_json'
        )

        PJSIPGlobalSettingsView.service = PJSIPGlobalSettingsService(
            clients['accent_confd']
        )
        PJSIPGlobalSettingsView.register(
            general_settings, route_base='/pjsip_global_settings'
        )
        register_flaskview(general_settings, PJSIPGlobalSettingsView)

        PJSIPSystemSettingsView.service = PJSIPSystemSettingsService(
            clients['accent_confd']
        )
        PJSIPSystemSettingsView.register(
            general_settings, route_base='/pjsip_system_settings'
        )
        register_flaskview(general_settings, PJSIPSystemSettingsView)

        IaxGeneralSettingsView.service = IaxGeneralSettingsService(
            clients['accent_confd']
        )
        IaxGeneralSettingsView.register(
            general_settings, route_base='/iax_general_settings'
        )
        register_flaskview(general_settings, IaxGeneralSettingsView)

        SCCPGeneralSettingsView.service = SCCPGeneralSettingsService(
            clients['accent_confd']
        )
        SCCPGeneralSettingsView.register(
            general_settings, route_base='/sccp_general_settings'
        )
        register_flaskview(general_settings, SCCPGeneralSettingsView)

        VoicemailGeneralSettingsView.service = VoicemailGeneralSettingsService(
            clients['accent_confd']
        )
        VoicemailGeneralSettingsView.register(
            general_settings, route_base='/voicemail_general_settings'
        )
        register_flaskview(general_settings, VoicemailGeneralSettingsView)

        FeaturesGeneralSettingsView.service = FeaturesGeneralSettingsService(
            clients['accent_confd']
        )
        FeaturesGeneralSettingsView.register(
            general_settings, route_base='/features_general_settings'
        )
        register_flaskview(general_settings, FeaturesGeneralSettingsView)

        ConfBridgeGeneralSettingsView.service = ConfBridgeGeneralSettingsService(
            clients['accent_confd']
        )
        ConfBridgeGeneralSettingsView.register(
            general_settings, route_base='/confbridge_general_settings'
        )
        register_flaskview(general_settings, ConfBridgeGeneralSettingsView)

        TimezoneListingView.service = TimezoneService(clients['accent_confd'])
        TimezoneListingView.register(general_settings, route_base='/timezones_listing')
        register_flaskview(general_settings, TimezoneListingView)
        register_listing_url(
            'timezone', 'general_settings.TimezoneListingView:list_json'
        )

        core.register_blueprint(general_settings)
