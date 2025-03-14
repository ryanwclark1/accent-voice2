# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
import signal
import threading
from functools import partial
from types import FrameType
from typing import TYPE_CHECKING

from accent import plugin_helpers
from accent.consul_helpers import ServiceCatalogRegistration
from accent.token_renewer import TokenRenewer
from accent_auth_client import Client as AuthClient

from accent_webhookd import celery

from . import auth
from .bus import BusConsumer
from .rest_api import CoreRestApi, api

if TYPE_CHECKING:
    from .types import WebhookdConfigDict

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, config: WebhookdConfigDict) -> None:
        self._stopping_thread: threading.Thread | None = None
        # NOTE: Celery must be spawned before anything else, to ensure
        # we don't fork the process after some database/rabbitmq connection
        # have been established
        celery.configure(config)
        self._celery_process = celery.spawn_workers(config)

        self._service_discovery_args = [
            'accent-webhookd',
            config.get('uuid'),
            config['consul'],
            config['service_discovery'],
            config['bus'],
            lambda: True,
        ]

        self._auth_client = AuthClient(**config['auth'])
        self._token_renewer = TokenRenewer(self._auth_client)
        if not config['auth'].get('master_tenant_uuid'):
            self._token_renewer.subscribe_to_next_token_details_change(
                auth.init_master_tenant
            )
        self._token_renewer.subscribe_to_token_change(self._auth_client.set_token)
        self._bus_consumer = BusConsumer(name='accent_webhookd', **config['bus'])
        self.rest_api = CoreRestApi(config)
        self._service_manager = plugin_helpers.load(
            namespace='accent_webhookd.services',
            names=config['enabled_services'],
            dependencies={
                'api': api,
                'bus_consumer': self._bus_consumer,
                'config': config,
                'auth_client': self._auth_client,
            },
        )
        plugin_helpers.load(
            namespace='accent_webhookd.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'api': api,
                'auth_client': self._auth_client,
                'bus_consumer': self._bus_consumer,
                'config': config,
                'service_manager': self._service_manager,
                'next_token_change_subscribe': self._token_renewer.subscribe_to_next_token_change,
            },
        )

    def run(self) -> None:
        logger.info('accent-webhookd starting...')
        signal.signal(signal.SIGTERM, partial(_signal_handler, self))
        signal.signal(signal.SIGINT, partial(_signal_handler, self))
        try:
            with ServiceCatalogRegistration(*self._service_discovery_args):
                with self._bus_consumer, self._token_renewer:
                    self.rest_api.run()
        finally:
            logger.info('accent-webhookd stopping...')
            self._celery_process.terminate()
            logger.debug('waiting for remaining threads/subprocesses...')
            self._celery_process.join()
            if self._stopping_thread:
                self._stopping_thread.join()
            logger.debug('all threads and subprocesses stopped.')

    def stop(self, reason: str) -> None:
        logger.warning('Stopping accent-webhookd: %s', reason)
        self._stopping_thread = threading.Thread(target=self.rest_api.stop, name=reason)
        self._stopping_thread.start()


def _signal_handler(controller: Controller, signum: int, frame: FrameType) -> None:
    controller.stop(reason=signal.Signals(signum).name)
