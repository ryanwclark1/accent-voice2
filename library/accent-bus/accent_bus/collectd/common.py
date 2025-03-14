# collectd/common.py
from abc import abstractmethod
from typing import ClassVar

from pydantic import BaseModel, field_validator


class CollectdEvent(BaseModel):
    """
    Base Collectd Event.

    Subclasses must define the following attributes:
      * name
      * routing_key_fmt
      * plugin
      * type_

    Args:
        content (dict | None, optional): Content of the collectd event.

    """

    routing_key_fmt: ClassVar[str]
    interval: int = 10
    plugin_instance: str | None = None
    time: str | int = "N"
    type_instance: str | None = None
    values: tuple[str, ...] = ()
    content: dict | None = None

    @property
    @abstractmethod
    def plugin(self) -> str:
        """Returns the plugin name. To be implemented by subclasses."""
        ...

    @property
    @abstractmethod
    def type_(self) -> str:
        """Returns the type. To be implemented by subclasses."""
        ...

    @field_validator("time")
    def time_must_be_valid(cls, v: str | int) -> str | int:
        """Validator to ensure the time attribute is valid."""
        if v != "N" and not isinstance(v, int):
            raise ValueError("time must be 'N' or an integer")
        return v

    def is_valid(self) -> bool:
        """
        Checks if the CollectdEvent is valid.

        Returns:
           bool: True if valid, False otherwise.
        """
        return (
            self.plugin is not None
            and self.plugin_instance is not None
            and self.type_ is not None
            and self.type_instance is not None
            and (self.time == "N" or isinstance(self.time, int))
            and len(self.values) > 0
        )

    def __str__(self) -> str:
        """
        String representation of the Collectd event.

        Returns:
            str: String describing the Collectd Event.
        """
        content = ", ".join(
            [
                f"plugin='{self.plugin}'",
                f"plugin_instance='{self.plugin_instance}'",
                f"type='{self.type_}'",
                f"type_instance='{self.type_instance}'",
                f"values={self.values}",
            ]
        )
        return f"CollectdEvent({content})"

    def generate_payload(self, service_uuid: str) -> str:
        """
        Generates the collectd payload string.

        Args:
            service_uuid: The UUID of the service.

        Returns:
            str: collectd formatted string

        Raises:
            ValueError: If event is not valid.
        """
        if not self.is_valid():
            raise ValueError(self)

        host = service_uuid

        plugin = self.plugin
        if self.plugin_instance:
            plugin = f"{self.plugin}-{self.plugin_instance}"

        type_ = f"{self.type_}-{self.type_instance}"
        interval = self.interval
        time = self.time
        values = ":".join(self.values)

        return f"PUTVAL {host}/{plugin}/{type_} interval={interval} {time}:{values}"
