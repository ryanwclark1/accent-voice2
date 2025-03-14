# src/accent_chatd/plugins/teams_presence/bus_consume.py


from accent_auth_client import Client as AuthClient
from accent_confd_client import Client as ConfdClient

from accent_chatd.core.bus import BusConsumer
from accent_chatd.services.teams import TeamsService

logger = make_logger(__name__)


class BusEventHandler:
    def __init__(
        self,
        bus: BusConsumer,
        teams_service: TeamsService,
        auth_client: AuthClient,
        confd_client: ConfdClient,
    ):
        self.bus = bus
        self.service = teams_service
        self.auth_client = auth_client
        self.confd_client = confd_client

    # No longer need _register_async_handler, as the consumer handles it.
    async def on_external_auth_added(self, payload):
        user_uuid, auth_name = payload.values()

        if auth_name != "microsoft":
            return

        logger.debug("connecting user `%s`", user_uuid)
        try:
            # You need a user token here, to create the subscription.
            # Get the tenant uuid, use that to get the user token.
            user_config = await self.confd_client.users(user_uuid).get(recurse=True)
            tenant_uuid = user_config["tenant_uuid"]
            # temp_token = self.auth_client.token.new( # No longer creating temporary token
            #   expiration=120,
            #   tenant_id=tenant_uuid
            # )
            # user_token = temp_token['token']
            # Use actual auth
            await self.service.create_subscription(user_uuid, tenant_uuid, "dummy")

        except Exception:
            logger.exception("an exception occured while creating subscription")

    async def on_external_auth_deleted(self, payload):
        user_uuid, auth_name = payload.values()
        if auth_name != "microsoft":
            return
        logger.debug("disconnecting user `%s`", user_uuid)
        try:
            # Delete subscription, and user token.
            user_config = await self.confd_client.users(user_uuid).get(recurse=True)
            tenant_uuid = user_config["tenant_uuid"]
            # temp_token = self.auth_client.token.new( # No longer needed.
            #   expiration=120,
            #   tenant_id=tenant_uuid
            # )
            # user_token = temp_token['token']
            await self.service.delete_subscription(
                user_uuid, "dummy"
            )  # Pass dummy token
        except Exception:
            logger.exception("an exception occured while deleting a subscription")
