# Copyright 2023 Accent Communications

import logging

from accent_bus.resources.switchboard.event import (
    SwitchboardHeldCallAnsweredEvent,
    SwitchboardHeldCallsUpdatedEvent,
    SwitchboardQueuedCallAnsweredEvent,
    SwitchboardQueuedCallsUpdatedEvent,
)

from .http import held_call_schema, queued_call_schema

logger = logging.getLogger(__name__)


class SwitchboardsNotifier:
    def __init__(self, bus):
        self._bus = bus

    def queued_calls(self, tenant_uuid, switchboard_uuid, calls):
        logger.debug(
            'Notifying updated queued calls for switchboard %s: %s calls',
            switchboard_uuid,
            len(calls),
        )

        items = queued_call_schema.dump(calls, many=True)
        event = SwitchboardQueuedCallsUpdatedEvent(items, switchboard_uuid, tenant_uuid)
        self._bus.publish(event)

    def queued_call_answered(
        self, tenant_uuid, switchboard_uuid, operator_call_id, queued_call_id
    ):
        logger.debug(
            'Queued call %s in switchboard %s answered by %s',
            queued_call_id,
            switchboard_uuid,
            operator_call_id,
        )

        event = SwitchboardQueuedCallAnsweredEvent(
            operator_call_id, queued_call_id, switchboard_uuid, tenant_uuid
        )
        self._bus.publish(event)

    def held_calls(self, tenant_uuid, switchboard_uuid, calls):
        logger.debug(
            'Notifying updated held calls for switchboard %s: %s calls',
            switchboard_uuid,
            len(calls),
        )

        items = held_call_schema.dump(calls, many=True)
        event = SwitchboardHeldCallsUpdatedEvent(items, switchboard_uuid, tenant_uuid)
        self._bus.publish(event)

    def held_call_answered(
        self, tenant_uuid, switchboard_uuid, operator_call_id, held_call_id
    ):
        logger.debug(
            'Held call %s in switchboard %s answered by %s',
            held_call_id,
            switchboard_uuid,
            operator_call_id,
        )

        event = SwitchboardHeldCallAnsweredEvent(
            operator_call_id, held_call_id, switchboard_uuid, tenant_uuid
        )
        self._bus.publish(event)
