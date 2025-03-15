# src/accent_chatd/plugins/presences/plugin.py

import logging

# from accent_chatd.plugins.presences.notifier import PresenceNotifier # Not using for now.
from accent_auth_client import Client as AuthClient
from accent_confd_client import Client as ConfdClient

from accent_chatd.core.plugin import Plugin
from accent_chatd.plugins.presences.bus_consume import BusEventHandler
from accent_chatd.plugins.presences.http import (
    PresenceItemResource,
    PresenceListResource,
)
from accent_chatd.services.presences import PresenceService

logger = logging.getLogger(__name__)


class Plugin(Plugin):
    def load(self, dependencies):
        api = dependencies["app"]
        config = dependencies["config"]
        dao = dependencies["dao"]
        bus_consumer = dependencies["bus_consumer"]
        bus_publisher = dependencies["bus_publisher"]
        # status_aggregator = dependencies['status_aggregator']
        # status_validator.set_config(status_aggregator, config) # Not using.

        # notifier = PresenceNotifier(bus_publisher) # Not using for now.

        service = PresenceService(
            dao.user, bus_publisher, bus_consumer
        )  # Pass consumer
        # token_changed_subscribe = dependencies['token_changed_subscribe']
        # next_token_changed_subscribe = dependencies['next_token_changed_subscribe']
        auth = AuthClient(**config["auth"])
        confd = ConfdClient(**config["confd"])
        # token_changed_subscribe(auth.set_token)
        # token_changed_subscribe(confd.set_token)

        # initiator = Initiator(dao, auth, amid, confd) # Removed initiator
        # status_aggregator.add_provider(initiator.provide_status) # Removed

        # if initialization['enabled']: # Removed initialization
        #     thread_manager = dependencies['thread_manager']
        #     initiator_thread = InitiatorThread(initiator)
        #     thread_manager.manage(initiator_thread)

        bus_event_handler = BusEventHandler(
            bus_consumer, service, auth, confd
        )  # Pass aio
        bus_event_handler.subscribe()

        api.add_api_route(
            "/users/presences",
            PresenceListResource(service).get,
            methods=["GET"],
            tags=["presences"],
        )

        api.add_api_route(
            "/users/{user_uuid}/presences",
            PresenceItemResource(service).get,
            methods=["GET"],
            tags=["presences"],
        )

        api.add_api_route(
            "/users/{user_uuid}/presences",
            PresenceItemResource(service).put,
            methods=["PUT"],
            tags=["presences"],
        )
