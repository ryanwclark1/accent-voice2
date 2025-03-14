# accent_bus/resources/common/event.py
# Copyright 2025 Accent Communications

"""Common event definitions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .abstract import EventProtocol

if TYPE_CHECKING:
    from collections.abc import Mapping

    from .types import UUIDStr


class ServiceEvent(EventProtocol):
    """### Service-level event base class.

    These events are intended for internal use by services and will never
    make it through the websocket.
    """

    def __init__(self, content: Mapping | None = None) -> None:
        """Initialize a ServiceEvent.

        Args:
          content (Mapping, optional): Event Content

        """
        self.content = content or {}


class TenantEvent(ServiceEvent):
    """### Tenant-level event base class.

    These events are intended for *all* users of the specified tenant.  They will be
    dispatched to all it's connected users by setting `user_uuid:*` in the headers.

    #### Required property:
        - tenant_uuid
    """

    def __init__(self, content: Mapping | None, tenant_uuid: UUIDStr) -> None:
        """Initialize a TenantEvent.

        Args:
            content (Mapping, optional): The event content.
            tenant_uuid (UUIDStr): The tenant UUID.

        """
        super().__init__(content)
        if tenant_uuid is None:
            msg = "tenant_uuid must have a value"
            raise ValueError(msg)
        self.tenant_uuid = str(tenant_uuid)
        setattr(self, "user_uuid:*", True)


class UserEvent(TenantEvent):
    """### User-level event base class.

    These events are intended for a single user from a specific tenant.  They will be
    dispatched through the websocket to the user by setting `user_uuid:{uuid}`
    in the headers.

    #### Required properties:
        - tenant_uuid
        - user_uuid
    """

    def __init__(
        self,
        content: Mapping | None,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr | None,
    ) -> None:
        """Initialize a UserEvent.

        Args:
           content (Mapping, optional): Content.
           tenant_uuid (UUIDStr): tenant UUID.
           user_uuid (UUIDStr | None): user UUID.

        """
        super().__init__(content, tenant_uuid)
        delattr(self, "user_uuid:*")
        self.user_uuid = str(user_uuid) if user_uuid else None

    @property
    def headers(self) -> dict:
        """Return the event headers.
        Sets the `user_uuid:{uuid}` header for the user.

        Returns:
          dict: event headers.

        """
        headers = super().headers
        uuid = headers.pop("user_uuid")
        if uuid:
            headers[f"user_uuid:{uuid}"] = True
        return headers


class MultiUserEvent(TenantEvent):
    """### User-level event base class (targetting multiple users).

    These events are intended for multiple users from a specific tenant.
    They will be dispatched through the websocket by setting `user_uuid:{uuid} = True`
    in the headers for all intended users.

    #### Required properties:
        - tenant_uuid
        - list of user_uuids
    """

    __slots__ = ("user_uuids",)

    def __init__(
        self,
        content: Mapping | None,
        tenant_uuid: UUIDStr,
        user_uuids: list[UUIDStr],
    ) -> None:
        """Initialize a MultiUserEvent.

        Args:
            content: Event content.
            tenant_uuid: tenant UUID.
            user_uuids:  list of user UUIDs.

        Raises:
          ValueError: if user_uuids is not a list

        """
        super().__init__(content, tenant_uuid)
        delattr(self, "user_uuid:*")
        if not isinstance(user_uuids, list):
            msg = "user_uuids must be a list of uuids"
            raise ValueError(msg)
        self.user_uuids = [str(user_uuid) for user_uuid in user_uuids]

    @property
    def headers(self) -> dict:
        """Return the event headers.
        Sets the `user_uuid:{uuid} = True` header for each user.

        Returns:
           dict: event headers.

        """
        headers = super().headers
        for user_uuid in self.user_uuids:
            headers[f"user_uuid:{user_uuid}"] = True
        return headers
