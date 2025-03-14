# resources/common/abstract.py
import logging
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)


# --- Event Protocol ---
class EventProtocol(BaseModel):
    """Protocol definition for events.

    Ensures all events have necessary properties and methods.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )  # Needed for ClassVar, routing and acl.

    content: dict
    name: ClassVar[str]
    routing_key_fmt: ClassVar[str]
    required_acl_fmt: ClassVar[str]

    @property
    def routing_key(self) -> str:
        """Calculates the routing key for the event.

        Returns:
            str: The routing key.

        """

    @property
    def required_access(self) -> str:
        """Defines the required access level for the event.

        Returns:
            str:  access level.

        """

    @property
    def headers(self) -> dict:
        """Generates headers for the event message.

        Returns:
            dict: A dictionary of headers.

        """
        headers = dict(vars(self))  # instance attributes
        headers["name"] = self.name  # Add the event name
        return headers

    def marshal(self) -> dict:
        """Marshals the event data into a dictionary.

        Returns:
             dict: The event data.

        """
        return self.model_dump()  # Use Pydantic's model_dump
