# resources/plugins/events.py
from typing import ClassVar

from pydantic import UUID4, BaseModel

from accent_bus.resources.common.event import ServiceEvent


class PluginProgressContent(BaseModel):
    """Content for plugin install/uninstall progress events.

    Attributes:
        uuid (UUID4): Plugin UUID
        status (str): Installation status.
        errors (dict, optional): Error details.

    """

    uuid: UUID4
    status: str
    errors: dict | None = None


class PluginInstallProgressEvent(ServiceEvent):
    """Event for reporting plugin installation progress."""

    service: ClassVar[str] = "plugind"
    name: ClassVar[str] = "plugin_install_progress"
    routing_key_fmt: ClassVar[str] = "plugin.install.{uuid}.{status}"
    content: PluginProgressContent

    def __init__(
        self, plugin_uuid: UUID4, status: str, errors: dict | None = None, **data
    ):
        content = PluginProgressContent(uuid=plugin_uuid, status=status, errors=errors)
        super().__init__(content=content.model_dump(), **data)


class PluginUninstallProgressEvent(ServiceEvent):
    """Event for reporting plugin uninstallation progress."""

    service: ClassVar[str] = "plugind"
    name: ClassVar[str] = "plugin_uninstall_progress"
    routing_key_fmt: ClassVar[str] = "plugin.uninstall.{uuid}.{status}"
    content: PluginProgressContent

    def __init__(
        self, plugin_uuid: UUID4, status: str, errors: dict | None = None, **data
    ):
        content = PluginProgressContent(uuid=plugin_uuid, status=status, errors=errors)
        super().__init__(content=content.model_dump(), **data)
