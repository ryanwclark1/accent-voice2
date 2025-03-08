# accent_auth/services/token.py

import logging
import time
from typing import Any

from accent_auth.db import DAO
from accent_auth import exceptions
from accent_auth.token import Token

# from accent_auth.services.user import UserService  # Remove circular import
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import cast, select
from sqlalchemy.ext.asyncio import AsyncSession  # Add missing import

logger = logging.getLogger(__name__)


class TokenService:  # No longer inherits from BaseService
    def __init__(self, config, dao: DAO, bus_publisher, user_service: Any):
        # super().__init__(dao) # Removed super call
        self._dao = dao
        self._config = config
        self._bus_publisher = bus_publisher
        self._user_service = user_service
        self._default_expiration = config["default_token_lifetime"]
        self._max_user_sessions = config["max_user_concurrent_sessions"]

    async def new_token(
        self, backend, login, args, session: AsyncSession
    ):  # Added session
        metadata = backend.get_metadata(login, args)
        logger.debug("metadata for %s: %s", login, metadata)

        auth_id = metadata["auth_id"]
        pbx_user_uuid = metadata.get("pbx_user_uuid")
        accent_uuid = metadata["accent_uuid"]
        tenant_uuid = metadata.get("tenant_uuid")
        purpose = metadata.get("purpose")

        if is_uuid(auth_id) and purpose in (
            "user",
            "external_api",
        ):  # added () to make more readable
            sessions = await self._dao.session.count(user_uuid=auth_id, session=session)
            if sessions >= self._max_user_sessions:
                raise exceptions.MaxConcurrentSessionsReached(auth_id)

        args["acl"] = await self._get_acl(args["backend"], session=session)
        args["metadata"] = metadata

        acl = backend.get_acl(login, args)
        expiration = args.get("expiration", self._default_expiration)
        current_time = time.time()

        session_payload = {}
        if tenant_uuid:
            session_payload["tenant_uuid"] = tenant_uuid
        if args.get("mobile"):
            session_payload["mobile"] = args["mobile"]

        token_payload = {
            "auth_id": auth_id,
            "pbx_user_uuid": pbx_user_uuid,
            "accent_uuid": accent_uuid,
            "expire_t": current_time + expiration,
            "issued_t": current_time,
            "acl": acl or [],
            "metadata": metadata,
            "user_agent": args["user_agent"],
            "remote_addr": args["remote_addr"],
        }

        if args.get("access_type", "online") == "offline":
            body = {
                "backend": args["backend"],
                "login": args["real_login"]
                if args.get("real_login")
                else args["login"],
                "client_id": args["client_id"],
                "user_uuid": metadata["uuid"],
                "user_agent": args["user_agent"],
                "remote_addr": args["remote_addr"],
                "mobile": args["mobile"],
            }
            try:
                refresh_token = await self._dao.refresh_token.create(
                    session=session, **body
                )
            except:
                refresh_token = (
                    await self._dao.refresh_token.get_existing_refresh_token(
                        args["client_id"], metadata["uuid"], session=session
                    )
                )
            else:
                # TODO: Fix event name
                event = RefreshTokenCreatedEvent(
                    body["client_id"], body["mobile"], tenant_uuid, body["user_uuid"]
                )
                self._bus_publisher.publish(event)
            token_payload["refresh_token_uuid"] = refresh_token.uuid

        token_uuid, session_uuid = await self._dao.token.create(
            token_payload,
            session_payload,
            refresh_token_uuid=args.get("refresh_token", None)
            or token_payload.get("refresh_token_uuid", None),
            session=session,
        )
        token = Token(token_uuid, session_uuid=session_uuid, **token_payload)

        user_uuid = auth_id if is_uuid(auth_id) else None
        event = SessionCreatedEvent(
            session_uuid,
            session_payload.get("mobile", False),
            session_payload["tenant_uuid"],
            user_uuid,
        )
        self._bus_publisher.publish(event)

        return token

    async def new_token_internal(
        self, expiration=None, acl=None, db: AsyncSession = None
    ):
        expiration = expiration if expiration is not None else self._default_expiration
        acl = acl or []
        current_time = time.time()
        token_args = {
            "auth_id": "accent-auth",
            "pbx_user_uuid": None,
            "accent_uuid": None,
            "expire_t": current_time + expiration,
            "issued_t": current_time,
            "acl": acl,
            "metadata": {"tenant_uuid": self.top_tenant_uuid},
            "user_agent": "accent-auth-internal",
            "remote_addr": "127.0.0.1",
        }
        session_args = {}
        token_uuid, session_uuid = await self._dao.token.create(
            token_args, session_args, session=db
        )
        token = Token(token_uuid, session_uuid=session_uuid, **token_args)
        return token

    async def get(
        self, token_uuid: str, required_access: str | None, db: AsyncSession
    ) -> Token:
        """Retrieves and validates a token."""
        token_data = await self._dao.token.get(token_uuid, session=db)
        if not token_data:
            logger.debug("Rejecting unknown token")
            raise exceptions.UnknownTokenException()

        token = Token(**token_data)

        if token.is_expired():
            logger.debug("Rejecting token: expired")
            raise exceptions.UnknownTokenException()

        if not token.matches_required_access(required_access):
            logger.debug("Rejecting token: forbidden access")
            raise exceptions.MissingAccessTokenException(required_access)

        return token

    async def check_scopes(
        self, token_uuid: str, scopes: list[str], db: AsyncSession
    ) -> tuple[Token, dict]:
        """Checks a token against a list of scopes."""
        token_data = await self._dao.token.get(token_uuid, session=db)
        if not token_data:
            raise exceptions.UnknownTokenException()

        token = Token(**token_data)

        if token.is_expired():
            raise exceptions.UnknownTokenException()

        scope_statuses = {
            scope: token.matches_required_access(scope) for scope in set(scopes)
        }

        return token, scope_statuses

    async def remove_token(self, token_uuid: str, db: AsyncSession) -> None:
        """Revokes (deletes) a token."""
        token, session = await self._dao.token.delete(token_uuid, session=db)
        if not session:
            return

        event = SessionDeletedEvent(
            session["uuid"], session["tenant_uuid"], token["auth_id"]
        )
        self._bus_publisher.publish(event)

    async def _get_acl(self, backend_name, db: AsyncSession):
        # 21.14: deprecated
        policy_name = self._config.get("backend_policies", {}).get(backend_name)

        if not policy_name:
            policy_name = self._config["default_user_policy"]

        if not policy_name:
            return []

        policy = await self._dao.policy.find_by(name=policy_name, session=db)
        if not policy:
            logger.info(
                'Unknown policy name "%s" configured for backend "%s"',
                policy_name,
                backend_name,
            )
            return []
        return policy.acl

    async def assert_has_tenant_permission(
        self, token: dict, tenant: str, db: AsyncSession
    ) -> None:
        """Asserts that the given tenant is allowed for this token."""

        if not tenant:
            return

        # internal token emitted by accent-auth
        if token["auth_id"] == "accent-auth":
            return

        user_uuid = token["auth_id"]
        if not await self._user_service.user_has_subtenant(
            user_uuid, tenant, db=db
        ):  # Pass db
            logger.debug("Rejecting token: forbidden tenant")
            raise exceptions.MissingTenantTokenException(tenant)

    async def list_refresh_tokens(self, db: AsyncSession = None, **kwargs):
        return await self._dao.refresh_token.list_(session=db, **kwargs)

    async def count_refresh_tokens(self, db: AsyncSession = None, **kwargs):
        return await self._dao.refresh_token.count(session=db, **kwargs)

    async def delete_refresh_token_by_uuid(self, uuid: str, db: AsyncSession):
        return await self._dao.refresh_token.delete_by_uuid(
            uuid=uuid, session=db
        )  # Added session
