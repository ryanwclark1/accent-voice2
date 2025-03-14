# accent_bus/resources/ami/event.py
# Copyright 2025 Accent Communications

"""AMI events."""

from accent_bus.resources.common.event import ServiceEvent


class AMIEvent(ServiceEvent):
    """AMI event."""

    service = "amid"
    name = "{ami_event}"
    routing_key_fmt = "ami.{name}"

    def __init__(self, ami_event: str, variables: dict[str, str]) -> None:
        """Initialize the AMI event.

        Args:
            ami_event (str): The AMI event name.
            variables (dict[str, str]): The event variables.

        """
        self.name = type(self).name.format(ami_event=ami_event)
        super().__init__(variables)
