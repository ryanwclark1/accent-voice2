# Copyright 2023 Accent Communications

import logging
import signal
import threading

from accent import plugin_helpers
from flask_babel import lazy_gettext as l_

from accent_ui.core.client import engine_clients
from accent_ui.core.form import (
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
from accent_ui.helpers.destination import register_destination_form
from accent_ui.helpers.error import (
    GENERIC_PATTERN_ERRORS,
    RESOURCES,
    SPECIFIC_PATTERN_ERRORS,
    URL_TO_NAME_RESOURCES,
    ConfdErrorExtractor,
    ErrorExtractor,
    ErrorTranslator,
)

from .http_server import Server

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, config):
        self.server = Server(config)
        self._stopping_thread = None
        plugin_helpers.load(
            namespace='accent_ui.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'config': config,
                'flask': self.server.get_app(),
                'clients': engine_clients,
            },
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

    def run(self):
        logger.info('accent-ui starting...')
        try:
            self.server.run()
        finally:
            logger.info('accent-ui stopping...')
            if self._stopping_thread:
                self._stopping_thread.join()

    def stop(self, reason):
        logger.warning('Stopping accent-ui: %s', reason)
        self._stopping_thread = threading.Thread(target=self.server.stop, name=reason)
        self._stopping_thread.start()


def _signal_handler(controller, signum, frame):
    controller.stop(reason=signal.Signals(signum).name)
