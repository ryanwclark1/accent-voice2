# Copyright 2023 Accent Communications

from __future__ import annotations

from accent.pubsub import CallbackCollector
from accent.status import Status
from accent_confd_client import Client as ConfdClient

from accent_calld.types import PluginDependencies, StatusDict

from .bus import EventHandler
from .http import LineEndpoints, TrunkEndpoints
from .notifier import EndpointStatusNotifier
from .services import ConfdCache, EndpointsService, NotifyingStatusCache


class Plugin:
    def load(self, dependencies: PluginDependencies) -> None:
        api = dependencies['api']
        ari = dependencies['ari']
        config = dependencies['config']
        status_aggregator = dependencies['status_aggregator']
        token_changed_subscribe = dependencies['token_changed_subscribe']
        bus_consumer = dependencies['bus_consumer']
        bus_publisher = dependencies['bus_publisher']

        confd_client = ConfdClient(**config['confd'])
        token_changed_subscribe(confd_client.set_token)

        confd_cache = ConfdCache(confd_client)
        notifier = EndpointStatusNotifier(bus_publisher, confd_cache)

        status_cache = NotifyingStatusCache(notifier.endpoint_updated, ari.client)
        endpoints_service = EndpointsService(confd_cache, status_cache)

        self._async_tasks_completed = False
        startup_callback_collector = CallbackCollector()
        ari.client_initialized_subscribe(startup_callback_collector.new_source())
        startup_callback_collector.subscribe(status_cache.initialize)
        startup_callback_collector.subscribe(self._set_async_tasks_completed)

        event_handler = EventHandler(status_cache, confd_cache)
        event_handler.subscribe(bus_consumer)

        status_aggregator.add_provider(self._provide_status)

        api.add_resource(
            TrunkEndpoints,
            '/trunks',
            resource_class_args=[
                endpoints_service,
            ],
        )

        api.add_resource(
            LineEndpoints,
            '/lines',
            resource_class_args=[
                endpoints_service,
            ],
        )

    def _set_async_tasks_completed(self) -> None:
        self._async_tasks_completed = True

    def _provide_status(self, status: StatusDict) -> None:
        value = Status.ok if self._async_tasks_completed else Status.fail
        status['plugins']['endpoints']['status'] = value
