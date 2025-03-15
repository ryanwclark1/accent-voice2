# src/accent_chatd/services/teams.py
import logging

from accent_chatd.api.teams_presence.client import MicrosoftGraphClient

logger = logging.getLogger(__name__)


class TeamsService:
    def __init__(self, graph_client: MicrosoftGraphClient):
        self._graph_client = graph_client
        # Replace the below with aiohttp.
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
        return

    async def create_subscription(self, user_uuid: str):
        # We will implement subscription creation in the next step.
        logger.info("Creating subscription")
        await self.connect_user(
            user_uuid, "some_ms_teams_id"
        )  # Add to the connected list.
        return

    async def delete_subscription(self, user_uuid: str):
        logger.info("Deleting subscription")
        await self.disconnect_user(user_uuid)
