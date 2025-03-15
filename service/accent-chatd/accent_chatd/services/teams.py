# src/accent_chatd/services/teams.py
import asyncio
import logging
import uuid
from datetime import datetime, timedelta, timezone
from accent_auth_client import Client as AuthClient  # Import

from accent_chatd.api.teams_presence.client import MicrosoftGraphClient
from accent_chatd.dao.teams_subscription import TeamsSubscriptionDAO
from accent_chatd.models.teams_subscription import TeamsSubscription

logger = logging.getLogger(__name__)

DEFAULT_EXPIRATION = 3600  # 1 hour in seconds
RENEWAL_THRESHOLD = 600  # Renew subscriptions 10 minutes before they expire


class TeamsService:
    def __init__(
        self,
        graph_client: MicrosoftGraphClient,
        subscription_dao: TeamsSubscriptionDAO,
        auth_client: AuthClient,
    ):
        self._graph_client = graph_client
        self._subscription_dao = subscription_dao
        self._auth_client = auth_client
        self._connected_users = {}  # Temporary storage for connected users. {user_uuid: ms_teams_user_id}

    def is_connected(self, user_uuid: str) -> bool:
        """Checks if a user is currently connected to Teams integration."""
        return user_uuid in self._connected_users

    async def connect_user(self, user_uuid: str, teams_user_id: str):
        self._connected_users[user_uuid] = teams_user_id

    async def disconnect_user(self, user_uuid: str):
        if user_uuid in self._connected_users:
            del self._connected_users[user_uuid]

    def user_uuid_from_teams(self, teams_user_id: str) -> str | None:
        for user_uuid, ms_teams_user_id in self._connected_users.items():
            if ms_teams_user_id == teams_user_id:
                return user_uuid
        return None

    async def fetch_teams_presence(self, teams_user_id: str) -> dict | None:
        """Fetches presence information from Microsoft Teams."""
        # try:
        #   # Replace with actual API call using self._graph_client, when implemented
        #   presence_data = await self._graph_client.get(
        #       f"/communications/presences/{teams_user_id}", "dummy_token"
        #   )
        #   return presence_data
        # except Exception as e:
        #   logger.error(f"Failed to fetch presence for {teams_user_id}: {e}")
        #   return None
        logger.info("Getting teams presence data.")
        return {"availability": "Available"}  # Dummy response for now

    async def update_presence(self, state: str, user_uuid: str):
        """Updates the user's presence in the database."""
        # Placeholder: Replace with actual database update logic using your DAO
        logger.info(f"Updating presence for user {user_uuid} to {state}")
        # await self._user_dao.update_presence(user_uuid, state) # Call the user DAO here

    async def create_subscription(
        self, user_uuid: str, tenant_uuid: str, user_token: str
    ) -> None:
        """Creates a Microsoft Graph subscription for presence updates."""
        logger.info(f"Creating subscription for user {user_uuid}")

        # 1. Get the MS Teams User ID (This is a placeholder - you'll need to
        #    get this from the authentication flow, likely when the user
        #    connects their MS Teams account).
        # Get the access token/teams user id from our auth_client
        try:
            external_auth = self._auth_client.external.get(
                "microsoft", user_uuid, tenant_uuid
            )
            ms_teams_user_id = external_auth["microsoft_user_id"]
            access_token = external_auth["access_token"]  # Get access token
        except Exception as e:
            logger.error(f"Could not retrieve teams information for user: {user_uuid}")
            return

        # 2. Check if a subscription already exists for this user.
        existing_subscription = await self._subscription_dao.get_by_user_uuid(user_uuid)
        if existing_subscription:
            logger.info(
                f"Subscription already exists for user {user_uuid}, deleting..."
            )
            await self.delete_subscription(
                user_uuid, access_token
            )  # Delete the old one.  You might want to *update* it instead.

        # 3. Create the subscription.
        client_state = str(uuid.uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=DEFAULT_EXPIRATION)
        notification_url = f"http://127.0.0.1:9304/1.0/users/{user_uuid}/teams/presence"  # Replace with your actual URL.

        subscription_data = {
            "changeType": "updated",
            "notificationUrl": notification_url,
            "resource": f"/communications/presences?$filter=id in ('{ms_teams_user_id}')",
            "expirationDateTime": expires_at.isoformat(),
            "clientState": client_state,
            "latestSupportedTlsVersion": "v1_2",
            "includeResourceData": False,
        }
        try:
            # Make the API call using the graph client.
            response = await self._graph_client.post(
                "/subscriptions", access_token, json_data=subscription_data
            )  # use token here.
            # 4. Store the subscription in the database.
            subscription = TeamsSubscription(
                user_uuid=user_uuid,
                subscription_id=response["id"],
                client_state=client_state,
                resource=response["resource"],
                expiration_date_time=datetime.fromisoformat(
                    response["expirationDateTime"].replace("Z", "+00:00")
                ),  # Ensure timezone awareness
                ms_teams_user_id=ms_teams_user_id,
            )

            await self._subscription_dao.create(subscription)
            await self.connect_user(user_uuid, ms_teams_user_id)
            logger.info(f"Created subscription for user {user_uuid}: {response}")

        except Exception as e:
            logger.exception(f"Failed to create subscription for user {user_uuid}: {e}")
            # Consider raising a custom exception here, or handling the error in a way that's appropriate
            # for your application (e.g., retrying, notifying an administrator, etc.).

    async def delete_subscription(self, user_uuid: str, user_token: str) -> None:
        """Deletes a Microsoft Graph subscription."""
        logger.info(f"Deleting subscription for user {user_uuid}")
        subscription = await self._subscription_dao.get_by_user_uuid(user_uuid)

        if subscription:
            try:
                # Make API call to delete.
                await self._graph_client.delete(
                    f"/subscriptions/{subscription.subscription_id}", user_token
                )
                await self._subscription_dao.delete(subscription)
                await self.disconnect_user(user_uuid)  # Disconnect
                logger.info(
                    f"Deleted subscription {subscription.subscription_id} for user {user_uuid}"
                )
            except Exception as e:
                logger.exception(
                    f"Failed to delete subscription {subscription.subscription_id}: {e}"
                )
        else:
            logger.warning(f"No subscription found for user {user_uuid} to delete")

    async def renew_subscriptions(self):
        """Renews expiring subscriptions."""
        logger.info("Checking for expiring Teams presence subscriptions...")
        now = datetime.now(timezone.utc)
        renewal_threshold = now + timedelta(seconds=RENEWAL_THRESHOLD)

        async with self._subscription_dao.session() as session:  # Get a session
            subscriptions = await session.execute(
                select(TeamsSubscription).where(
                    TeamsSubscription.expiration_date_time <= renewal_threshold
                )
            )
            subscriptions = subscriptions.scalars().all()

            for subscription in subscriptions:
                logger.info(
                    f"Renewing subscription {subscription.subscription_id} for user {subscription.user_uuid}"
                )
                try:
                    # 1. Construct the request to Microsoft Graph.  You only need to send the new expiration time.
                    expires_at = datetime.now(timezone.utc) + timedelta(
                        seconds=DEFAULT_EXPIRATION
                    )
                    update_data = {"expirationDateTime": expires_at.isoformat()}

                    # 2. Make the API call using the graph client.  You'll need a valid token!
                    # Get a valid token.
                    user_token = self.auth_client.token.new(expiration=120)
                    response = await self._graph_client.patch(
                        f"/subscriptions/{subscription.subscription_id}",
                        user_token["token"],  # Replace with a valid token
                        json_data=update_data,
                    )
                    # print("RESPONSE:", response) # debug

                    # 3. Update the subscription in the database.
                    subscription.expiration_date_time = datetime.fromisoformat(
                        response["expirationDateTime"].replace(
                            "Z", "+00:00"
                        )  # Ensure timezone awareness.
                    )
                    await self._subscription_dao.update(subscription)
                    logger.info(f"Renewed subscription {subscription.subscription_id}")

                except Exception as e:
                    logger.exception(
                        f"Failed to renew subscription {subscription.subscription_id}: {e}"
                    )
                    # Handle the error appropriately (e.g., retry, log, notify)
