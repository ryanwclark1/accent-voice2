# Copyright 2023 Accent Communications

import logging
from functools import partial
from threading import Thread

from accent import plugin_helpers, pubsub
from accent.config_helper import get_accent_uuid
from accent.consul_helpers import ServiceCatalogRegistration
from accent.status import StatusAggregator, TokenStatus
from accent.token_renewer import TokenRenewer
from accent_auth_client import Client as AuthClient

from .ari_ import CoreARI
from .asyncio_ import CoreAsyncio
from .auth import init_master_tenant
from .bus import CoreBusConsumer, CoreBusPublisher
from .collectd import CollectdPublisher
from .http_server import HTTPServer, api
from .service_discovery import self_check

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, config):
        accent_uuid = get_accent_uuid(logger)
        self._stopping_thread = None
        auth_client = AuthClient(**config['auth'])
        self.asyncio = CoreAsyncio()
        self.bus_consumer = CoreBusConsumer.from_config(config['bus'])
        self.bus_publisher = CoreBusPublisher.from_config(config['uuid'], config['bus'])
        self.ari = CoreARI(config['ari'], self.bus_consumer)
        self.collectd = CollectdPublisher.from_config(
            config['uuid'], config['bus'], config['collectd']
        )
        self.http_server = HTTPServer(config)
        self.status_aggregator = StatusAggregator()
        self.token_renewer = TokenRenewer(auth_client)
        self.token_status = TokenStatus()
        self._service_registration_params = [
            'accent-calld',
            accent_uuid,
            config['consul'],
            config['service_discovery'],
            config['bus'],
            partial(self_check, config),
        ]

        self._pubsub = pubsub.Pubsub()
        plugin_helpers.load(
            namespace='accent_calld.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'api': api,
                'ari': self.ari,
                'asyncio': self.asyncio,
                'bus_publisher': self.bus_publisher,
                'bus_consumer': self.bus_consumer,
                'collectd': self.collectd,
                'config': config,
                'status_aggregator': self.status_aggregator,
                'pubsub': self._pubsub,
                'token_changed_subscribe': self.token_renewer.subscribe_to_token_change,
                'next_token_changed_subscribe': self.token_renewer.subscribe_to_next_token_change,
            },
        )

        if not config['auth'].get('master_tenant_uuid'):
            self.token_renewer.subscribe_to_next_token_details_change(
                init_master_tenant
            )

    def run(self):
        logger.info('accent-calld starting...')
        self.token_renewer.subscribe_to_token_change(
            self.token_status.token_change_callback
        )
        self.status_aggregator.add_provider(self.ari.provide_status)
        self.status_aggregator.add_provider(self.bus_consumer.provide_status)
        self.status_aggregator.add_provider(self.token_status.provide_status)
        self.ari.init_client()
        asyncio_thread = Thread(target=self.asyncio.run, name='asyncio_thread')
        asyncio_thread.start()
        try:
            with self.token_renewer:
                with self.bus_consumer, self.collectd:
                    with ServiceCatalogRegistration(*self._service_registration_params):
                        self.http_server.run()
        finally:
            logger.info('accent-calld stopping...')
            self._pubsub.publish('stopping', None)
            self.asyncio.stop()
            self.ari.stop()
            logger.debug('joining asyncio thread')
            asyncio_thread.join()
            if self._stopping_thread:
                self._stopping_thread.join()
            logger.debug('done joining')

    def stop(self, reason):
        logger.warning('Stopping accent-calld: %s', reason)
        self._stopping_thread = Thread(target=self.http_server.stop, name=reason)
        self._stopping_thread.start()
