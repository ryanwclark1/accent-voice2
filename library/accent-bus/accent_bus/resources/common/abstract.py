# resources/common/abstract.py
from abc import ABC, abstractmethod
from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class EventProtocol(BaseModel, ABC):
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
    @abstractmethod
    def routing_key(self) -> str:
        """Calculates the routing key for the event.

        Returns:
            str: The routing key.

        """
        ...

    @property
    @abstractmethod
    def required_access(self) -> str:
        """Defines the required access level for the event.

        Returns:
            str:  access level.

        """
        ...

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
