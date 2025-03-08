# Copyright 2023 Accent Communications

from accent_bus.resources.call_logd.events import CallLogRetentionUpdatedEvent

from .schemas import RetentionSchema


class RetentionNotifier:
    def __init__(self, bus):
        self._bus = bus

    def updated(self, retention):
        payload = RetentionSchema().dump(retention)
        event = CallLogRetentionUpdatedEvent(payload, retention.tenant_uuid)
        self._bus.publish(event)
