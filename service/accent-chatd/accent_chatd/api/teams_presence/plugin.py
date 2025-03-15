# src/accent_chatd/plugins/teams_presence/plugin.py
import logging

from accent_auth_client import Client as AuthClient
from accent_confd_client import Client as ConfdClient

from accent_chatd.core.bus import (
    get_bus_consumer,
    BusConsumer,
    get_bus_publisher,
    BusPublisher,
)
from accent_chatd.dao.user import UserDAO
from accent_chatd.plugins.presences.services import (
    PresenceService,
)  # Import Presence Service
from accent_chatd.services.teams import TeamsService
from .bus_consume import BusEventHandler
from .http import TeamsPresenceResource
from .log import make_logger

# from .notifier import TeamsNotifier  # Removed for now.

logger = make_logger(__name__)


class Plugin:
    def load(self, dependencies):
        # aio = dependencies['aio'] # No longer need.
        api = dependencies["api"]
        config = dependencies["config"]
        dao = dependencies["dao"]
        bus_consumer: BusConsumer = get_bus_consumer()  # Use dependency injection
        bus_publisher: BusPublisher = get_bus_publisher()  # Use dependency injection
        status_aggregator = dependencies["status_aggregator"]
        # status_validator.set_config(status_aggregator, config) # Not used currently.

        # notifier = TeamsNotifier(aio, bus_publisher)
        presence_service = PresenceService(
            dao.user, bus_publisher, bus_consumer
        )  # Pass consumer
        # token_changed_subscribe = dependencies['token_changed_subscribe']
        # next_token_changed_subscribe = dependencies['next_token_changed_subscribe']
        auth_client = AuthClient(**config["auth"])
        confd_client = ConfdClient(**config["confd"])
        # token_changed_subscribe(auth.set_token)
        # token_changed_subscribe(confd.set_token)

        teams_service = TeamsService(
            MicrosoftGraphClient(config["teams_presence"]["microsoft_graph_url"]),
            dao.teams_subscription,
        )
        # teams_service.initialize() # Removed

        events_handler = BusEventHandler(
            bus_consumer, teams_service, auth_client, confd_client
        )  # Pass aio
        events_handler.subscribe()

        api.add_resource(
            TeamsPresenceResource,
            "/users/<user_uuid>/teams/presence",
            resource_class_args=(teams_service,),
        )
