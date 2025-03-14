# resources/services/event.py
from typing import ClassVar

from pydantic import BaseModel

from accent_bus.resources.common.event import ServiceEvent


class ServiceRegisteredContent(BaseModel):
    """Content of the service registered event"""

    service_name: str
    service_id: str
    address: str
    port: int
    tags: list[str]


class ServiceRegisteredEvent(ServiceEvent):
    """Event for when a service registers."""

    name: ClassVar[str] = "service_registered"
    routing_key_fmt: ClassVar[str] = "service.registered.{service_name}"
    content: ServiceRegisteredContent

    def __init__(
        self,
        service_name: str,
        service_id: str,
        advertise_address: str,
        advertise_port: int,
        tags: list[str],
        **data,
    ):
        content = ServiceRegisteredContent(
            service_name=service_name,
            service_id=service_id,
            address=advertise_address,
            port=advertise_port,
            tags=tags,
        )
        super().__init__(content=content.model_dump(), **data)


class ServiceDeregisteredContent(BaseModel):
    """Content for service de-registered events."""

    service_name: str
    service_id: str
    tags: list[str]


class ServiceDeregisteredEvent(ServiceEvent):
    """Event for when a service deregisters."""

    name: ClassVar[str] = "service_deregistered"
    routing_key_fmt: ClassVar[str] = (
        "service.registered.{service_name}"  # Inconsistency with the original, should be deregistered
    )
    content: ServiceDeregisteredContent

    def __init__(self, service_name: str, service_id: str, tags: list[str], **data):
        content = ServiceDeregisteredContent(
            service_name=service_name, service_id=service_id, tags=tags
        )
        super().__init__(content=content.model_dump(), **data)
