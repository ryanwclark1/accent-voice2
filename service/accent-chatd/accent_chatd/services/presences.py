# src/accent_chatd/services/presences.py
import datetime
import logging

from accent_chatd.core.bus import BusConsumer, BusPublisher  # Import BusConsumer
from accent_chatd.dao.user import UserDAO
from accent_chatd.models import User
from accent_chatd.schemas.presence import UserPresence

logger = logging.getLogger(__name__)


class PresenceService:
    def __init__(
        self, user_dao: UserDAO, bus_publisher: BusPublisher, bus_consumer: BusConsumer
    ):
        self._user_dao = user_dao
        self._bus_publisher = bus_publisher
        self._bus_consumer = bus_consumer  # Add consumer.
        self.subscribe_to_events()  # Call on init.

    async def list_(self, tenant_uuids: list[str], **filter_parameters) -> list[User]:
        return await self._user_dao.list_(tenant_uuids, **filter_parameters)

    async def count(self, tenant_uuids: list[str], **filter_parameters) -> int:
        return await self._user_dao.count(tenant_uuids, **filter_parameters)

    async def get(self, tenant_uuids: list[str], user_uuid: str) -> User:
        return await self._user_dao.get(tenant_uuids, user_uuid)

    async def update(self, user: User) -> User:
        user.last_activity = datetime.datetime.now(datetime.UTC)
        await self._user_dao.update(user)
        await self._notify_updated(user)  # Call notification
        return user

    async def _notify_updated(self, user: User):
        # Convert model to pydantic schema.
        payload = UserPresence.model_validate(user).model_dump()
        # Use the async bus publisher.
        await self._bus_publisher.publish(
            payload,
            routing_key=f"chatd.users.{user.uuid}.presence.updated",
            headers={
                "name": "chatd_presence_updated",
                "tenant_uuid": str(user.tenant_uuid),
                f"user_uuid:{user.uuid}": True,
            },
        )

    # Placeholder event handlers
    async def _on_user_created(self, payload: dict):
        logger.info(f"Received user_created event: {payload}")
        # Add logic to create user in the database

    async def _on_user_deleted(self, payload: dict):
        logger.info(f"Received user_deleted event: {payload}")
        # Add logic to delete user from the database

    def subscribe_to_events(self):
        """Subscribe to bus events."""
        events = [
            ("user_created", self._on_user_created),
            ("user_deleted", self._on_user_deleted),
        ]

        for event, handler in events:
            self._bus_consumer.subscribe(event, handler)
