# accent_auth/token.py

import logging
import threading
import time
from datetime import datetime, timezone
from functools import partial

from accent_auth.db import DAO
from accent_auth.services.user import UserService
from accent_auth import exceptions
from accent_auth.bus import BusPublisher

# Use an appropriate event for expired tokens if you have one
from accent_bus.resources.auth.events import SessionDeletedEvent
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class Token:
    """Represents an authentication token."""

    def __init__(
        self,
        uuid: str,
        auth_id: str,
        session_uuid: str,
        acl: list[str],
        expire_t: int | None,
        issued_t: int | None,
        metadata: dict | None = None,
        pbx_user_uuid: str | None = None,
        accent_uuid: str | None = None,
        user_agent: str | None = None,
        remote_addr: str | None = None,
        refresh_token: str | None = None,
        refresh_token_uuid: str | None = None,
    ):
        self.token = uuid  # Better naming consistency.
        self.auth_id = auth_id
        self.pbx_user_uuid = pbx_user_uuid
        self.accent_uuid = accent_uuid
        self.issued_at = issued_t
        self.expires_at = expire_t
        self.metadata = metadata or {}  # Ensure metadata is not None
        self.acl = acl
        self.session_uuid = session_uuid
        self.user_agent = user_agent
        self.remote_addr = remote_addr
        self.refresh_token = refresh_token
        self.refresh_token_uuid = refresh_token_uuid

        from .auth.permissions import AccessCheck  # Moved to avoid circular import

        self._access_check = AccessCheck(self.auth_id, self.session_uuid, self.acl)

    def is_expired(self) -> bool:
        """Checks if the token is expired."""
        return self.expires_at is not None and time.time() > self.expires_at

    def matches_required_access(self, required_access: str | None) -> bool:
        """Checks if the token grants the required access."""
        return self._access_check.matches_required_access(required_access)


class ExpiredTokenRemover:
    """Removes expired tokens and sessions from the database."""

    def __init__(
        self, config: dict, dao: DAO, bus_publisher: BusPublisher, saml_service: Any
    ):
        self._dao = dao
        self._bus_publisher = bus_publisher
        self._saml_service = saml_service
        self._cleanup_interval = config["token_cleanup_interval"]
        self._batch_size = config["token_cleanup_batch_size"]
        self._debug = config["debug"]
        if self._cleanup_interval < 1:
            return

        self._tombstone = threading.Event()
        self._thread = threading.Thread(target=self._loop)
        self._thread.daemon = True

    def start(self) -> None:
        """Starts the background thread for removing expired tokens."""
        if self._cleanup_interval > 0:
            self._thread.start()

    def stop(self) -> None:
        """Stops the background thread."""
        if self._cleanup_interval > 0:
            self._tombstone.set()
            self._thread.join()
            self._tombstone.clear()

    def _loop(self) -> None:
        while not self._tombstone.is_set():
            started = time.monotonic()

            try:
                asyncio.run(self._purge_expired_sessions())
                asyncio.run(self._purge_expired_saml_sessions())
            except Exception:
                logger.warning(
                    "%s: an exception occurred during execution",
                    self.__class__.__name__,
                    exc_info=self._debug,
                )

            elapsed = time.monotonic() - started

            if elapsed >= self._cleanup_interval:
                log_level = logging.WARNING
            else:
                log_level = logging.DEBUG
            logger.log(log_level, "ExpiredTokenRemover took %.5f seconds", elapsed)

            if elapsed < self._cleanup_interval:
                self._tombstone.wait(self._cleanup_interval - elapsed)

    async def _purge_expired_sessions(self) -> None:
        """Purges expired tokens and sessions from the database."""
        async with AsyncSessionLocal() as session:  # Use a new session
            async for (
                tokens,
                sessions,
            ) in self._dao.token.purge_expired_tokens_and_sessions(
                self._batch_size, session=session
            ):
                try:
                    for token, session_data in zip(tokens, sessions):
                        if token["session_uuid"] != session_data["uuid"]:
                            logger.warning("token and session mismatch")
                            continue

                        if "tenant_uuid" not in token["metadata"]:
                            logger.warning(
                                "invalid session %s: no tenant_uuid found",
                                session_data["uuid"],
                            )
                            continue

                        event = SessionDeletedEvent(
                            session_data["uuid"],
                            token["metadata"]["tenant_uuid"],
                            token["auth_id"],
                        )
                        self._bus_publisher.publish(event)  # Consider making this async
                    await session.commit()
                except Exception:
                    await session.rollback()
                    raise

    async def _purge_expired_saml_sessions(self) -> None:
        await self._saml_service.clean_pending_requests()
