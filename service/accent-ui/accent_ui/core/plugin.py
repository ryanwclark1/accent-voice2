# Copyright 2023 Accent Communications

from accent import plugin_helpers
from flask_babel import lazy_gettext as l_

from ..helpers.destination import register_destination_form
from ..helpers.error import (
    GENERIC_PATTERN_ERRORS,
    RESOURCES,
    SPECIFIC_PATTERN_ERRORS,
    URL_TO_NAME_RESOURCES,
    ConfdErrorExtractor,
    ErrorExtractor,
    ErrorTranslator,
)
from .client import engine_clients
from .form import (
    ApplicationCallBackDISADestination,
    ApplicationDestination,
    ApplicationDirectoryDestination,
    ApplicationDISADestination,
    ApplicationFaxToMailDestination,
    ApplicationVoicemailDestination,
    CustomDestination,
    HangupDestination,
    NoneDestination,
    register_destination_form_application,
)


class CorePlugin:
    def load(self, dependencies):
        enabled_plugins = dependencies['config_plugins']['enabled_plugins']
        app = dependencies['flask']
        plugin_helpers.load(
            namespace='accent_engine.plugins',
            names=enabled_plugins,
            dependencies={'flask': app, 'clients': engine_clients},
        )

        ErrorExtractor.register_url_to_name_resources(URL_TO_NAME_RESOURCES)
        ErrorTranslator.register_resources(RESOURCES)

        ConfdErrorExtractor.register_generic_patterns(GENERIC_PATTERN_ERRORS)
        ConfdErrorExtractor.register_specific_patterns(SPECIFIC_PATTERN_ERRORS)

        register_destination_form(
            'application', l_('Application'), ApplicationDestination
        )
        register_destination_form('hangup', l_('Hangup'), HangupDestination)
        register_destination_form('custom', l_('Custom'), CustomDestination)
        register_destination_form('none', l_('None'), NoneDestination, position=0)

        register_destination_form_application(
            'callback_disa',
            l_('CallBack DISA'),
            ApplicationCallBackDISADestination,
        )
        register_destination_form_application(
            'directory',
            l_('Directory'),
            ApplicationDirectoryDestination,
        )
        register_destination_form_application(
            'disa',
            l_('DISA'),
            ApplicationDISADestination,
        )
        register_destination_form_application(
            'fax_to_mail',
            l_('Fax to Mail'),
            ApplicationFaxToMailDestination,
        )
        register_destination_form_application(
            'voicemail',
            l_('Voicemail'),
            ApplicationVoicemailDestination,
        )
