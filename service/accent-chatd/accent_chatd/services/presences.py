# src/accent_chatd/services/presences.py
import datetime
from typing import List

from accent_chatd.dao.user import UserDAO
from accent_chatd.core.bus import BusPublisher, BusConsumer  # Import BusConsumer
from accent_chatd.schemas.presence import UserPresence
from accent_chatd.models import User, Tenant

import logging

logger = logging.getLogger(__name__)


class PresenceService:
    def __init__(
        self, user_dao: UserDAO, bus_publisher: BusPublisher, bus_consumer: BusConsumer
    ):
        self._user_dao = user_dao
        self._bus_publisher = bus_publisher
        self._bus_consumer = bus_consumer
        self.subscribe_to_events()

    async def list_(self, tenant_uuids: List[str], **filter_parameters) -> List[User]:
        return await self._user_dao.list_(tenant_uuids, **filter_parameters)

    async def count(self, tenant_uuids: List[str], **filter_parameters) -> int:
        return await self._user_dao.count(tenant_uuids, **filter_parameters)

    async def get(self, tenant_uuids: List[str], user_uuid: str) -> User:
        return await self._user_dao.get(tenant_uuids, user_uuid)

    async def update(self, user: User) -> User:
        user.last_activity = datetime.datetime.now(datetime.timezone.utc)
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

    # Event Handlers
    async def _on_user_created(self, payload: dict):
        logger.info(f"Received user_created event: {payload}")
        try:
            user_uuid = payload["uuid"]
            tenant_uuid = payload["tenant_uuid"]
            async with self._user_dao.session() as session:
                async with session.begin():
                    tenant = await session.execute(
                        select(Tenant).where(Tenant.uuid == tenant_uuid)
                    )
                    tenant = tenant.scalar_one_or_none()
                    if not tenant:
                        tenant = Tenant(uuid=tenant_uuid)
                        session.add(tenant)
                    # Check if user already exists (prevent race conditions on startup)
                    existing_user = await session.execute(
                        select(User).where(User.uuid == user_uuid)
                    )
                    existing_user = existing_user.scalar_one_or_none()

                    if not existing_user:
                        user = User(uuid=user_uuid, tenant=tenant, state="unavailable")
                        session.add(user)
                        logger.info(f"Created user {user_uuid} in tenant {tenant_uuid}")
                    else:
                        logger.info(f"User {user_uuid} already exists.")
        except Exception:
            logger.exception(
                f"Failed to create user {user_uuid} in tenant {tenant_uuid}"
            )

    async def _on_user_deleted(self, payload: dict):
        logger.info(f"Received user_deleted event: {payload}")
        try:
            user_uuid = payload["uuid"]
            tenant_uuid = payload["tenant_uuid"]
            # Get and delete
            async with self._user_dao.session() as session:
                async with session.begin():
                    user = await self._user_dao.get([tenant_uuid], user_uuid)
                    await self._user_dao.delete(user)
        except UnknownUserException:
            logger.warning(f"user with uuid {user_uuid} does not exist.")
        except Exception:
            logger.exception(
                f"Failed to delete user {user_uuid} in tenant {tenant_uuid}"
            )

    def subscribe_to_events(self):
        """Subscribe to bus events."""
        events = [
            ("user_created", self._on_user_created),
            ("user_deleted", self._on_user_deleted),
        ]

        for event, handler in events:
            self._bus_consumer.subscribe(event, handler)
