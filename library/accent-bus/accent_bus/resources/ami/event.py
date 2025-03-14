# resources/ami/event.py
from typing import ClassVar

from pydantic import BaseModel

from accent_bus.resources.common.event import ServiceEvent


class AMIEventContent(BaseModel):
    """Content of the AMI Event."""

    variables: dict[str, str]


class AMIEvent(ServiceEvent):
    """Represents an AMI event.

    Attributes:
        service (ClassVar[str]): The service that originates the event.
        name (str):  Event name
        routing_key_fmt (ClassVar[str]):  The routing key format
        variables (dict[str, str]): Event variables.

    """

    service: ClassVar[str] = "amid"
    name: ClassVar[str] = "{ami_event}"
    routing_key_fmt: ClassVar[str] = "ami.{name}"
    content: AMIEventContent

    def __init__(self, ami_event: str, variables: dict[str, str], **data):
        self.name = self.name.format(ami_event=ami_event)
        content = AMIEventContent(variables=variables)
        super().__init__(content=content.model_dump(), **data)

    @property
    def routing_key(self) -> str:
        """Calculates and returns the routing key for the AMI event.

        The routing key is dynamically generated based on the event name.
        """
        # Escape and format routing key using the inherited method.
        return super().routing_key
