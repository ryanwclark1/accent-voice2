# src/accent_chatd/plugins/teams_presence/bus_consume.py

import logging

from accent_auth_client import Client as AuthClient

# from accent_chatd.core.asyncio_ import CoreAsyncio # No longer needed.
from accent_chatd.core.bus import BusConsumer
from accent_chatd.services.teams import TeamsService

logger = logging.getLogger(__name__)


class BusEventHandler:
    def __init__(
        self,
        # aio: CoreAsyncio, # No longer need.
        bus: BusConsumer,
        teams_service: TeamsService,
        auth_client: AuthClient,
    ):
        # self.aio = aio
        self.bus = bus
        self.service = teams_service
        self.auth_client = auth_client

    # No longer need _register_async_handler, as the consumer handles it.
    async def on_external_auth_added(self, payload):
        user_uuid, auth_name = payload.values()

        if auth_name != "microsoft":
            return

        logger.debug("connecting user `%s`", user_uuid)
        try:
            # You need a user token here, to create the subscription.
            # This depends on how you are handling user login.
            # For *testing only*, we'll create a temporary token.  This is NOT secure.
            user_token = self.auth_client.token.new(expiration=120)
            user_token = user_token["token"]
            await self.service.create_subscription(
                user_uuid, "0000", user_token
            )  # TODO fix hardcoded

        except Exception:
            logger.exception("an exception occured while creating subscription")

    async def on_external_auth_deleted(self, payload):
        user_uuid, auth_name = payload.values()

        if auth_name != "microsoft":
            return

        logger.debug("disconnecting user `%s`", user_uuid)
        try:
            await self.service.delete_subscription(user_uuid)
        except Exception:
            logger.exception("an exception occured while deleting a subscription")

    def subscribe(self):
        events = (
            ("auth_user_external_auth_added", self.on_external_auth_added),
            ("auth_user_external_auth_deleted", self.on_external_auth_deleted),
        )

        for event, handler in events:
            self.bus.subscribe(event, handler)  # Use the subscribe method
