# Copyright 2023 Accent Communications

from __future__ import annotations

from ..common.event import ServiceEvent
from ..common.types import UUIDStr
from .types import PluginErrorDict


class PluginInstallProgressEvent(ServiceEvent):
    service = 'plugind'
    name = 'plugin_install_progress'
    routing_key_fmt = 'plugin.install.{uuid}.{status}'

    def __init__(
        self,
        plugin_uuid: UUIDStr,
        status: str,
        errors: PluginErrorDict | None = None,
    ):
        content = {'uuid': plugin_uuid, 'status': status}
        if errors:
            content.update(errors=errors)  # type: ignore[call-overload]
        super().__init__(content)


class PluginUninstallProgressEvent(ServiceEvent):
    service = 'plugind'
    name = 'plugin_uninstall_progress'
    routing_key_fmt = 'plugin.uninstall.{uuid}.{status}'

    def __init__(
        self,
        plugin_uuid: UUIDStr,
        status: str,
        errors: PluginErrorDict | None = None,
    ):
        content = {'uuid': plugin_uuid, 'status': status}
        if errors:
            content.update(errors=errors)  # type: ignore[call-overload]
        super().__init__(content)
