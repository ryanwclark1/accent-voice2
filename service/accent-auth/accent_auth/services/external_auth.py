# accent_auth/services/external_auth.py

import json
import logging
import threading
from collections.abc import Sequence
from functools import partial
from typing import Any

import marshmallow
from accent_auth.db import DAO

# from accent_auth.services.helpers import BaseService, TemplateFormatter  # REMOVED
from accent_auth import exceptions
from sqlalchemy.ext.asyncio import AsyncSession

# try:
#    import websocket  # Keep, but we'll use it differently
# except ImportError:
#    pass
from accent_bus.resources.auth.events import (
    UserExternalAuthAddedEvent,
    UserExternalAuthAuthorizedEvent,
    UserExternalAuthDeletedEvent,
)

logger = logging.getLogger(__name__)


class _OAuth2Synchronizer:  # Keep this for now
    def __init__(self, config, bus_publisher):
        self._url_tpl = config["oauth2_synchronization_ws_url_template"]
        self._bus_publisher = bus_publisher

    def synchronize(self, event, state, success_cb):
        logger.debug("starting synchronization")
        # NOTE: This is still using a thread.  Ideally, this would be
        # fully async, but that depends on the websocket library.  For
        # now, I'm keeping the thread, but this is something you should
        # consider refactoring later to use an async websocket library
        # like websockets.
        websocket_client_thread = threading.Thread(
            target=self._synchronize, args=(event, state, success_cb)
        )
        websocket_client_thread.daemon = True
        websocket_client_thread.start()
        logger.debug("synchronization started")

    def _synchronize(self, event, state, success_cb):
        url = self._url_tpl.format(state=state)
        logger.debug("waiting on external authentication to complete %s...", url)
        ws = websocket.WebSocketApp(
            url,
            on_message=partial(self._on_message, event, success_cb),
            on_error=self._on_error,
            on_close=self._on_close,
        )
        ws.run_forever()

    def _on_message(self, event, success_cb, ws, msg):
        logger.debug("ws message received: %s", msg)
        try:
            msg = json.loads(msg)
            success_cb(msg)
            # commit_or_rollback() # Removed, this will be handled in the lifespan event.
            headers = {"tenant_uuid": event.tenant_uuid}
            self._bus_publisher.publish(event, headers=headers)
        finally:
            ws.close()

    def _on_error(self, ws, error):
        logger.debug("ws error: %s", error)

    def _on_close(self, ws):
        logger.debug("ws closed")


class ExternalAuthService:  # Removed (BaseService)
    def __init__(
        self,
        dao: DAO,
        config: dict,
        bus_publisher=None,
        enabled_external_auth: Sequence[str] | None = None,
    ):
        # super().__init__(dao)  # REMOVED
        self._dao = dao
        self._bus_publisher = bus_publisher
        self._safe_models: dict[str, Any] = {}  # Keep for schema validation
        self._enabled_external_auth = enabled_external_auth or []
        self._enabled_external_auth_populated = False
        self._url_tpl = config["oauth2_synchronization_redirect_url_template"]
        self._oauth2_synchronizer = _OAuth2Synchronizer(config, bus_publisher)

    async def _get_user_tenant_uuid(
        self, user_uuid: str, db: AsyncSession
    ) -> str:  # Added session
        user = await self._dao.user.get(user_uuid, session=db)  # Added session
        if not user:
            raise exceptions.UnknownUserException(user_uuid)
        return user.tenant_uuid

    async def count(
        self, user_uuid: str, db: AsyncSession = None, **kwargs
    ) -> int:  # Added session
        await self._populate_enabled_external_auth(db=db)
        return await self._dao.external_auth.count(
            user_uuid, session=db, **kwargs
        )  # Added session

    async def count_connected_users(
        self,
        auth_type: str,
        scoping_tenant_uuid: str | None = None,
        recurse: bool = False,
        db: AsyncSession = None,
        **kwargs,
    ) -> int:
        await self._populate_enabled_external_auth(db=db)

        if scoping_tenant_uuid:
            kwargs["tenant_uuids"] = await self._get_scoped_tenant_uuids(
                scoping_tenant_uuid, recurse, db=db
            )

        return await self._dao.external_auth.count_connected_users(
            auth_type, session=db, **kwargs
        )  # Added session

    async def create(
        self, user_uuid: str, auth_type: str, data: dict, db: AsyncSession
    ) -> dict:  # Added session
        result = await self._dao.external_auth.create(
            user_uuid, auth_type, data, session=db
        )  # Added session
        tenant_uuid = await self._get_user_tenant_uuid(user_uuid, db=db)
        event = UserExternalAuthAddedEvent(auth_type, tenant_uuid, user_uuid)
        self._bus_publisher.publish(event)  # Consider async
        return result

    async def create_config(
        self, auth_type: str, data: dict, tenant_uuid: str, db: AsyncSession
    ) -> dict:  # Added session
        return await self._dao.external_auth_config.create(
            auth_type,
            data,
            tenant_uuid,
            session=db,  # Added session
        )

    async def delete(
        self, user_uuid: str, auth_type: str, db: AsyncSession
    ) -> None:  # Added session
        await self._dao.external_auth.delete(
            user_uuid, auth_type, session=db
        )  # Added session
        tenant_uuid = await self._get_user_tenant_uuid(user_uuid, db=db)
        event = UserExternalAuthDeletedEvent(auth_type, tenant_uuid, user_uuid)
        self._bus_publisher.publish(event)  # Consider async

    async def delete_config(
        self, auth_type: str, tenant_uuid: str, db: AsyncSession
    ) -> None:  # Added session
        await self._dao.external_auth_config.delete(
            auth_type, tenant_uuid, session=db
        )  # Added session

    async def get(
        self, user_uuid: str, auth_type: str, db: AsyncSession
    ) -> dict:  # Added session
        return await self._dao.external_auth.get(
            user_uuid, auth_type, session=db
        )  # Added session

    async def get_config(
        self, auth_type: str, tenant_uuid: str, db: AsyncSession
    ) -> dict:  # Added session
        return await self._dao.external_auth_config.get(
            auth_type, tenant_uuid, session=db
        )

    async def list_(
        self, user_uuid: str, db: AsyncSession, **kwargs
    ) -> list[dict]:  # Added session
        await self._populate_enabled_external_auth(db=db)
        raw_external_auth_info = await self._dao.external_auth.list_(
            user_uuid, session=db, **kwargs
        )
        result = []
        for external_auth in raw_external_auth_info:
            auth_type = external_auth["type"]
            enabled = external_auth["enabled"]
            Model = self._safe_models.get(auth_type)
            filtered_data = {}
            if Model:
                data = external_auth.get("data")
                try:
                    filtered_data = Model().load(data)
                except marshmallow.ValidationError as e:
                    filtered_data = e.valid_data
                    logger.info(
                        "Failed to parse %s data for user %s: %s",
                        auth_type,
                        user_uuid,
                        e.messages,
                    )
            result.append(
                {"type": auth_type, "data": filtered_data, "enabled": enabled}
            )
        return result

    async def list_connected_users(
        self,
        auth_type: str,
        scoping_tenant_uuid: str | None = None,
        recurse: bool = True,
        db: AsyncSession = None,
        **kwargs,
    ) -> list[str]:
        await self._populate_enabled_external_auth(db=db)

        if scoping_tenant_uuid:
            kwargs["tenant_uuids"] = await self._get_scoped_tenant_uuids(
                scoping_tenant_uuid, recurse, db=db
            )

        return await self._dao.external_auth.list_connected_users(
            auth_type, session=db, **kwargs
        )  # Added session

    async def update(
        self, user_uuid: str, auth_type: str, data: dict, db: AsyncSession
    ) -> dict:  # Added session
        await self.delete(
            user_uuid, auth_type, db=db
        )  # Easy way to ensure the type exists
        result = await self.create(user_uuid, auth_type, data, db=db)
        return result

    async def update_config(
        self, auth_type: str, data: dict, tenant_uuid: str, db: AsyncSession
    ) -> dict:  # Added session
        await self.delete_config(
            auth_type, tenant_uuid, db=db
        )  # Easy way to ensure the type exists
        result = await self.create_config(auth_type, data, tenant_uuid, db=db)
        return result

    def build_oauth2_redirect_url(self, auth_type):
        return self._url_tpl.format(auth_type=auth_type)

    async def _populate_enabled_external_auth(self, db: AsyncSession):
        if self._enabled_external_auth_populated:
            return
        await self._dao.external_auth_type.enable_all(
            self._enabled_external_auth, session=db
        )
        self._enabled_external_auth_populated = True

    def register_oauth2_callback(
        self, auth_type, user_uuid, state, cb, *args, **kwargs
    ):
        tenant_uuid = self._get_user_tenant_uuid(user_uuid)
        event = UserExternalAuthAuthorizedEvent(auth_type, tenant_uuid, user_uuid)
        self._oauth2_synchronizer.synchronize(
            event, state, partial(cb, *args, **kwargs)
        )

    def register_safe_auth_model(self, auth_type, model_class):
        self._safe_models[auth_type] = model_class

    async def _get_scoped_tenant_uuids(
        self, scoping_tenant_uuid: str, recurse: bool, db: AsyncSession
    ) -> list[str]:
        """Gets the UUIDs of all tenants visible from a scoping tenant.

        Args:
            scoping_tenant_uuid: The UUID of the scoping tenant.
            recurse: Whether to include subtenants recursively.

        Returns:
            A list of tenant UUIDs.
        """
        from accent_auth.services.tenant import TenantService  # Avoid circular import

        if not recurse:
            return [scoping_tenant_uuid]
        tenant_service = TenantService(
            self._dao, None, None
        )  # all_users_policies and bus publisher are not used
        visible_tenants = await tenant_service.list_sub_tenants(
            scoping_tenant_uuid, db=db
        )

        return visible_tenants
