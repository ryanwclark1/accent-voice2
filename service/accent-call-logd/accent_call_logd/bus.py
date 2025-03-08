# Copyright 2023 Accent Communications

from accent.status import Status
from accent_bus.consumer import BusConsumer as BaseConsumer
from accent_bus.publisher import BusPublisher as BasePublisher
from accent_bus.resources.call_logs.events import (
    CallLogCreatedEvent,
    CallLogUserCreatedEvent,
)

from accent_call_logd.plugins.cdr.schemas import CDRSchema


class BusConsumer(BaseConsumer):
    @classmethod
    def from_config(cls, config):
        name = 'accent-call-logd'
        return cls(name=name, **config)

    def provide_status(self, status):
        status['bus_consumer']['status'] = (
            Status.ok if self.consumer_connected() else Status.fail
        )


class BusPublisher(BasePublisher):
    @classmethod
    def from_config(cls, service_uuid, config):
        name = 'accent-call-logd'
        return cls(name=name, service_uuid=service_uuid, **config)

    def publish_call_log(self, *call_logs):
        for call_log in call_logs:
            payload = CDRSchema().dump(call_log)
            event = CallLogCreatedEvent(payload, call_log.tenant_uuid)
            super().publish(event)

            user_payload = CDRSchema(exclude=['tags']).dump(call_log)
            for participant in call_log.participants:
                user_event = CallLogUserCreatedEvent(
                    user_payload, call_log.tenant_uuid, participant.user_uuid
                )
                super().publish(user_event)
