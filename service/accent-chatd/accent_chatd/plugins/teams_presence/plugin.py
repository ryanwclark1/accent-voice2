# src/accent_chatd/plugins/teams_presence/plugin.py

import asyncio

from accent_auth_client import Client as AuthClient
from accent_confd_client import Client as ConfdClient

from accent_chatd.core.plugin import Plugin
from accent_chatd.plugins.presences.services import PresenceService

from .bus_consume import BusEventHandler
from .http import TeamsPresenceResource
from .log import make_logger
from .services import TeamsService

logger = make_logger(__name__)


class Plugin(Plugin):
    def load(self, dependencies):
        api = dependencies["app"]
        config = dependencies["config"]
        dao = dependencies["dao"]
        bus_consumer = dependencies["bus_consumer"]
        bus_publisher = dependencies["bus_publisher"]

        presence_service = PresenceService(
            dao.user, bus_publisher, bus_consumer
        )  # Pass consumer
        auth_client = AuthClient(**config["auth"])
        confd_client = ConfdClient(**config["confd"])

        teams_service = TeamsService(
            MicrosoftGraphClient(config["teams_presence"]["microsoft_graph_url"]),
            dao.teams_subscription,
            auth_client,
            presence_service,  # Pass the presence service
        )
        # Start the subscription renewal task.  This is the *correct* place to do this.
        asyncio.create_task(teams_service.renew_subscriptions())

        events_handler = BusEventHandler(
            bus_consumer, teams_service, auth_client, confd_client
        )
        events_handler.subscribe()

        api.add_api_route(
            "/users/<user_uuid>/teams/presence",
            TeamsPresenceResource(teams_service).post,
            methods=["POST"],
            tags=["teams_presence"],
        )
