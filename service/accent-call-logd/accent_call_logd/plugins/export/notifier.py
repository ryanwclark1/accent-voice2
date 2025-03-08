# Copyright 2023 Accent Communications

from accent_bus.resources.call_logd.events import (
    CallLogExportCreatedEvent,
    CallLogExportUpdatedEvent,
)

from .schemas import ExportSchema


class ExportNotifier:
    def __init__(self, bus):
        self._bus = bus

    def created(self, export):
        payload = ExportSchema().dump(export)
        event = CallLogExportCreatedEvent(payload, export.tenant_uuid)
        self._bus.publish(event)

    def updated(self, export):
        payload = ExportSchema().dump(export)
        event = CallLogExportUpdatedEvent(payload, export.tenant_uuid)
        self._bus.publish(event)
