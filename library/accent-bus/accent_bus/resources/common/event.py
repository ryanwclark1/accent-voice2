# resources/common/event.py
from typing import ClassVar

from pydantic import UUID4, Field

from .abstract import EventProtocol  # Import the protocol
from .routing_key import escape as escape_key


class ServiceEvent(EventProtocol):
    """Base class for service-level events (internal events).

    Args:
        content (dict): Content of the event.

    """

    service: ClassVar[str]  # Should be overridden in subclasses
    content: dict = {}  # All events will, at least, have content.

    def __init__(self, content: dict | None = None, **data):
        """Initialize ServiceEvent.

        Args:
            content (dict, optional): Content of the event. Defaults to None.
            **data: attributes of the event.

        """
        super().__init__(
            **data, content=content or {}
        )  # Initialize BaseModel and set content

    @property
    def required_access(self) -> str:
        """Returns the required access level (defaults to event name)."""
        return f"event.{self.name}"

    @property
    def routing_key(self) -> str:
        """Calculates the routing key, escaping necessary parts.

        Returns:
            str: The routing key.

        """
        variables = dict(**self.content)
        variables.update(vars(self), name=self.name)
        variables = {
            key: escape_key(value) if isinstance(value, str) else value
            for key, value in variables.items()
        }
        return self.routing_key_fmt.format(**variables)

    @property
    def headers(self) -> dict:
        """Generates the headers for the event, adding necessary keys and values.
        Removes the 'content' key, as it's not needed in headers.

        Returns:
            dict: A dictionary containing header information.

        """
        headers = super().headers
        del headers["content"]
        return headers


class TenantEvent(ServiceEvent):
    """Base class for tenant-level events.

    Attributes:
        tenant_uuid: The UUID of the tenant.

    """

    tenant_uuid: UUID4 = Field(..., description="The UUID of the tenant")
    # user_uuid is not a field here: it is part of the routing
    # and will be included in the headers and routing key.

    @property
    def headers(self) -> dict:
        """Tenant events do not require user filtering, they go to all tenant."""
        headers = super().headers
        # del headers["content"]
        headers["tenant_uuid"] = str(self.tenant_uuid)  # Fixed
        return headers


class UserEvent(TenantEvent):
    """Base class for user-level events.

    Attributes:
        user_uuid: The UUID of the user.  Can be None.

    """

    user_uuid: UUID4 | None = Field(
        default=None, description="The UUID of the user. Can be None."
    )

    @property
    def headers(self) -> dict:
        """Adds user_uuid:{uuid} = True to the headers for user-specific events."""
        headers = super().headers
        uuid = self.user_uuid
        if uuid:
            headers[f"user_uuid:{uuid}"] = True
        # del headers["content"]
        return headers


class MultiUserEvent(TenantEvent):
    """Base class for events targeting multiple users within a tenant.

    Attributes:
        user_uuids: A list of user UUIDs.

    """

    user_uuids: list[UUID4] = Field(..., description="List of user UUIDs")

    @property
    def user_uuids_str(self) -> list[str]:
        return [str(user_uuid) for user_uuid in self.user_uuids]

    @property
    def headers(self) -> dict:
        """Adds user_uuid:{uuid} = True for each user in user_uuids."""
        headers = super().headers
        for user_uuid in self.user_uuids_str:
            headers[f"user_uuid:{user_uuid}"] = True
        # del headers["content"]
        return headers
