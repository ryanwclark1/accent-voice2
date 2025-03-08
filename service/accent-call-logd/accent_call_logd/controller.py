# Copyright 2023 Accent Communications

import logging
import signal
import threading
import time
from functools import partial

from accent import plugin_helpers
from accent.status import StatusAggregator, TokenStatus
from accent.token_renewer import TokenRenewer
from accent_auth_client import Client as AuthClient
from accent_confd_client import Client as ConfdClient

from accent_call_logd import celery
from accent_call_logd.cel_interpretor import (
    default_interpretors,
)
from accent_call_logd.generator import CallLogsGenerator
from accent_call_logd.manager import CallLogsManager
from accent_call_logd.writer import CallLogsWriter

from .auth import init_master_tenant
from .bus import BusConsumer, BusPublisher
from .database.helpers import new_db_session
from .database.queries import DAO
from .http_server import HTTPServer, api, app

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, config):
        self.config = config
        self._stopping_thread = None
        DBSession = new_db_session(config['db_uri'])
        CELDBSession = new_db_session(config['cel_db_uri'])
        self.dao = DAO(DBSession, CELDBSession)
        writer = CallLogsWriter(self.dao)

        # NOTE: it is important to load the tasks before configuring the Celery app
        self.celery_task_manager = plugin_helpers.load(
            namespace='accent_call_logd.celery_tasks',
            names=config['enabled_celery_tasks'],
            dependencies={
                'config': self.config,
                'dao': self.dao,
                'app': celery.app,
            },
        )
        celery.configure(config)
        self._celery_process = celery.spawn_workers(config)

        auth_client = AuthClient(**config['auth'])
        confd_client = ConfdClient(**config['confd'])
        generator = CallLogsGenerator(
            confd_client,
            default_interpretors(),
        )
        self.token_renewer = TokenRenewer(auth_client)
        self.token_renewer.subscribe_to_token_change(confd_client.set_token)
        self.token_renewer.subscribe_to_next_token_details_change(
            generator.set_default_tenant_uuid
        )

        self.bus_publisher = BusPublisher.from_config(config['uuid'], config['bus'])
        self.bus_consumer = BusConsumer.from_config(config['bus'])
        self.manager = CallLogsManager(self.dao, generator, writer, self.bus_publisher)

        self._bus_subscribe()

        self.http_server = HTTPServer(config)
        if not app.config['auth'].get('master_tenant_uuid'):
            self.token_renewer.subscribe_to_next_token_details_change(
                init_master_tenant
            )

        self.status_aggregator = StatusAggregator()
        self.token_status = TokenStatus()
        plugin_helpers.load(
            namespace='accent_call_logd.plugins',
            names=config['enabled_plugins'],
            dependencies={
                'api': api,
                'config': config,
                'dao': self.dao,
                'token_renewer': self.token_renewer,
                'status_aggregator': self.status_aggregator,
                'bus_publisher': self.bus_publisher,
                'bus_consumer': self.bus_consumer,
            },
        )

    def run(self):
        logger.info('Starting accent-call-logd')
        signal.signal(signal.SIGTERM, partial(_signal_handler, self))
        signal.signal(signal.SIGINT, partial(_signal_handler, self))
        self.token_renewer.subscribe_to_token_change(
            self.token_status.token_change_callback
        )
        self.status_aggregator.add_provider(self.bus_consumer.provide_status)
        self.status_aggregator.add_provider(self.token_status.provide_status)
        self.status_aggregator.add_provider(celery.provide_status)
        self._update_db_from_config_file()

        try:
            with self.bus_consumer:
                with self.token_renewer:
                    self.http_server.run()
        finally:
            logger.info('Stopping accent-call-logd...')
            self._celery_process.terminate()
            self._celery_process.join()
            if self._stopping_thread:
                self._stopping_thread.join()

    def stop(self, reason):
        logger.warning('Stopping accent-call-logd: %s', reason)
        self._stopping_thread = threading.Thread(
            target=self.http_server.stop, name=reason
        )
        self._stopping_thread.start()

    def _update_db_from_config_file(self):
        with self.dao.helper.db_ready():
            config = self.dao.config.find_or_create()
            cdr_days = self.config['retention']['cdr_days']
            if cdr_days is not None:
                config.retention_cdr_days = cdr_days
                config.retention_cdr_days_from_file = True
            else:
                config.retention_cdr_days_from_file = False
            export_days = self.config['retention']['export_days']
            if export_days is not None:
                config.retention_export_days = export_days
                config.retention_export_days_from_file = True
            else:
                config.retention_export_days_from_file = False
            recording_days = self.config['retention']['recording_days']
            if recording_days is not None:
                config.retention_recording_days = recording_days
                config.retention_recording_days_from_file = True
            else:
                config.retention_recording_days_from_file = False
            self.dao.config.update(config)

    def _bus_subscribe(self):
        self.bus_consumer.subscribe('CEL', self._handle_linked_id_end)

    def _handle_linked_id_end(self, payload):
        if payload['EventName'] != 'LINKEDID_END':
            return

        linked_id = payload['LinkedID']
        start_time = time.time()
        try:
            self.manager.generate_from_linked_id(linked_id)
        except Exception:
            logger.exception(
                'Failed to generate call log for linkedid \"%s\"', linked_id
            )
        else:
            processing_time = time.time() - start_time
            logger.info(
                'Generated call log for linkedid \"%s\" in %.2fs',
                linked_id,
                processing_time,
            )


def _signal_handler(controller, signum, frame):
    controller.stop(reason=signal.Signals(signum).name)
