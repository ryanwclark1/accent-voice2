# Copyright 2023 Accent Communications

import logging
import signal
import threading
from functools import partial

from accent import plugin_helpers
from accent.consul_helpers import ServiceCatalogRegistration
from accent.status import StatusAggregator
from accent.token_renewer import TokenRenewer
from accent_auth_client import Client as AuthClient

from . import auth
from .http_server import CoreRestApi, api, app
from .stopper import Stopper

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, config):
        self._service_discovery_args = [
            'accent-setupd',
            config.get('uuid'),
            config['consul'],
            config['service_discovery'],
            config['bus'],
            lambda: True,
        ]
        self.rest_api = CoreRestApi(config)
        self.status_aggregator = StatusAggregator()
        self.stopper = Stopper(config['self_stop_delay'], self)
        auth_client = AuthClient(**config['auth'])
        self.token_renewer = TokenRenewer(auth_client)
        if not app.config['auth'].get('master_tenant_uuid'):
            self.token_renewer.subscribe_to_next_token_details_change(
                auth.init_master_tenant
            )
        plugin_helpers.load(
            namespace='accent_setupd.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'api': api,
                'config': config,
                'status_aggregator': self.status_aggregator,
                'stopper': self.stopper,
            },
        )
        self.stopper_thread = threading.Thread(target=self.stopper.wait)
        self.stopper_http_thread = None

    def run(self):
        logger.info('accent-setupd starting...')
        signal.signal(signal.SIGTERM, partial(_signal_handler, self))
        signal.signal(signal.SIGINT, partial(_signal_handler, self))
        self.status_aggregator.add_provider(auth.provide_status)
        self.stopper_thread.start()
        try:
            with self.token_renewer:
                with ServiceCatalogRegistration(*self._service_discovery_args):
                    self.rest_api.run()
        finally:
            logger.info('accent-setupd stopping...')
            logger.debug('joining stopper thread')
            self.stopper.cancel()
            self.stopper_thread.join()
            if self._stopper_http_thread:
                self._stopper_http_thread.join()

    def stop(self, reason):
        logger.warning('Stopping accent-setupd: %s', reason)
        self._stopper_http_thread = threading.Thread(
            target=self.rest_api.stop,
            name=reason,
        )
        self._stopper_http_thread.start()


def _signal_handler(controller, signum, frame):
    controller.stop(reason=signal.Signals(signum).name)
