# resources/common/event.py
from typing import ClassVar

from pydantic import UUID4, Field

from .abstract import EventProtocol
from .acl import escape as escape_acl
from .routing_key import escape as escape_key


class ServiceEvent(EventProtocol[dict]):  # ServiceEvent uses a dict for content
    """Base class for service-level events (internal events)."""

    service: ClassVar[str]  # Should be overridden in subclasses

    def __init__(self, content: dict | None = None, **data):
        super().__init__(content=content or {}, **data)

    @property
    def required_access(self) -> str:
        """Returns the required access level for the event.

        Returns:
            str: A string representing the required access level in the format "event.<event_name>".

        """
        return f"event.{self.name}"

    @property
    def routing_key(self) -> str:
        """Calculates the routing key, escaping necessary parts."""
        variables = dict(**self.content)
        variables.update(vars(self), name=self.name)
        variables = {
            key: escape_key(value) if isinstance(value, str) else value
            for key, value in variables.items()
        }
        return self.routing_key_fmt.format(**variables)

    @property
    def headers(self) -> dict:
        """Generates headers, excluding 'content'."""
        headers = super().headers
        del headers["content"]
        return headers


class TenantEvent(ServiceEvent):
    """Base class for tenant-level events."""

    tenant_uuid: UUID4 = Field(..., description="The UUID of the tenant")

    @property
    def headers(self) -> dict:
        """Adds tenant_uuid to headers."""
        headers = super().headers
        headers["tenant_uuid"] = str(self.tenant_uuid)
        return headers


class UserEvent(TenantEvent):
    """Base class for user-level events."""

    user_uuid: UUID4 | None = Field(
        default=None, description="The UUID of the user. Can be None."
    )

    @property
    def headers(self) -> dict:
        """Adds user_uuid:{uuid} = True to headers."""
        headers = super().headers
        if self.user_uuid:
            headers[f"user_uuid:{self.user_uuid}"] = True
        return headers


class MultiUserEvent(TenantEvent):
    """Base class for events targeting multiple users."""

    user_uuids: list[UUID4] = Field(..., description="List of user UUIDs")

    @property
    def user_uuids_str(self) -> list[str]:
        """Returns user_uuids as strings."""
        return [str(user_uuid) for user_uuid in self.user_uuids]

    @property
    def headers(self) -> dict:
        """Adds user_uuid:{uuid} = True for each user."""
        headers = super().headers
        for user_uuid in self.user_uuids_str:
            headers[f"user_uuid:{user_uuid}"] = True
        return headers
