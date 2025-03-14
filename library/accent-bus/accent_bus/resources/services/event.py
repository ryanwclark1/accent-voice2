# accent_bus/resources/services/event.py
# Copyright 2025 Accent Communications

"""Service events."""

from accent_bus.resources.common.event import ServiceEvent


class ServiceRegisteredEvent(ServiceEvent):
    """Event for when a service is registered."""

    name = "service_registered"
    routing_key_fmt = "service.registered.{service_name}"

    def __init__(
        self,
        service_name: str,
        service_id: str,
        advertise_address: str,
        advertise_port: int,
        tags: list[str],
    ) -> None:
        """Initialize the event.

        Args:
           service_name: Service Name
           service_id: Service ID
           advertise_address: Advertise Address
           advertise_port: Advertise Port
           tags: Tags

        """
        content = {
            "service_name": service_name,
            "service_id": service_id,
            "address": advertise_address,
            "port": advertise_port,
            "tags": tags,
        }
        super().__init__(content)


class ServiceDeregisteredEvent(ServiceEvent):
    """Event for when a service is deregistered."""

    name = "service_deregistered"
    routing_key_fmt = "service.registered.{service_name}"

    def __init__(self, service_name: str, service_id: str, tags: list[str]) -> None:
        """Initialize the event.

        Args:
           service_name: Service Name
           service_id: Service ID
           tags: Tags

        """
        content = {
            "service_name": service_name,
            "service_id": service_id,
            "tags": tags,
        }
        super().__init__(content)
