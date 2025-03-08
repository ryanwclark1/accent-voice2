# Copyright 2023 Accent Communications

import logging
from threading import Thread

from accent import plugin_helpers
from accent.config_helper import set_accent_uuid
from accent.status import StatusAggregator, TokenStatus
from accent.token_renewer import TokenRenewer
from accent_auth_client import Client as AuthClient

from .auth import init_master_tenant
from .bus import CoreBusConsumer
from .http_server import HTTPServer, api, app

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, config):
        self.config = config
        set_accent_uuid(config, logger)
        self.bus_consumer = CoreBusConsumer(config)
        self.status_aggregator = StatusAggregator()
        self.http_server = HTTPServer(self.config)
        app.config['authorized_subnets'] = self.config['rest_api']['authorized_subnets']
        auth_client = AuthClient(**config['auth'])
        self.token_renewer = TokenRenewer(auth_client)
        self.token_renewer.subscribe_to_token_change(self._on_token_change)

        self.token_status = TokenStatus()
        self.token_renewer.subscribe_to_token_change(
            self.token_status.token_change_callback
        )

        self.phone_plugins = []
        self.plugin_manager = plugin_helpers.load(
            namespace='accent_phoned.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'config': config,
                'api': api,
                'app': app,
                'token_changed_subscribe': self.token_renewer.subscribe_to_token_change,
                'bus_consumer': self.bus_consumer,
                'status_aggregator': self.status_aggregator,
                'phone_plugins': self.phone_plugins,
            },
        )

        if not config['auth'].get('master_tenant_uuid'):
            self.token_renewer.subscribe_to_next_token_details_change(
                init_master_tenant
            )

    def run(self):
        logger.debug('accent-phoned starting...')
        self.status_aggregator.add_provider(self.bus_consumer.provide_status)
        self.status_aggregator.add_provider(self.token_status.provide_status)
        bus_consumer_thread = Thread(
            target=self.bus_consumer.run, name='bus_consumer_thread'
        )
        bus_consumer_thread.start()
        try:
            with self.token_renewer:
                self.http_server.run()
        finally:
            logger.info('accent-phoned stopping...')
            self.bus_consumer.should_stop = True
            logger.debug('joining rest api thread...')
            self.http_server.join()
            logger.debug('joining bus consumer thread...')
            bus_consumer_thread.join()
            logger.debug('done joining.')

    def stop(self, reason):
        logger.warning('Stopping accent-phoned: %s', reason)
        self.http_server.stop()

    def _on_token_change(self, token_id):
        app.config['token'] = token_id
