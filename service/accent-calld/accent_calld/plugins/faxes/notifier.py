# Copyright 2023 Accent Communications

from accent_bus.resources.faxes.event import (
    FaxOutboundCreatedEvent,
    FaxOutboundFailedEvent,
    FaxOutboundSucceededEvent,
    FaxOutboundUserCreatedEvent,
    FaxOutboundUserFailedEvent,
    FaxOutboundUserSucceededEvent,
)


class FaxesNotifier:
    def __init__(self, bus_producer):
        self._bus_producer = bus_producer

    @staticmethod
    def _build_headers(fax_infos):
        return {'tenant_uuid': fax_infos['tenant_uuid']}

    def notify_fax_created(self, fax_infos):
        user_uuid = fax_infos['user_uuid']
        event = FaxOutboundCreatedEvent(fax_infos, fax_infos['tenant_uuid'])
        self._bus_producer.publish(event)

        if user_uuid:
            event = FaxOutboundUserCreatedEvent(
                fax_infos, fax_infos['tenant_uuid'], user_uuid
            )
            self._bus_producer.publish(event)

    def notify_fax_succeeded(self, fax_infos):
        user_uuid = fax_infos['user_uuid']
        event = FaxOutboundSucceededEvent(fax_infos, fax_infos['tenant_uuid'])
        self._bus_producer.publish(event)

        if user_uuid:
            event = FaxOutboundUserSucceededEvent(
                fax_infos, fax_infos['tenant_uuid'], user_uuid
            )
            self._bus_producer.publish(event)

    def notify_fax_failed(self, fax_infos):
        user_uuid = fax_infos['user_uuid']
        event = FaxOutboundFailedEvent(fax_infos, fax_infos['tenant_uuid'])
        self._bus_producer.publish(event)

        if user_uuid:
            event = FaxOutboundUserFailedEvent(
                fax_infos, fax_infos['tenant_uuid'], user_uuid
            )
            self._bus_producer.publish(event)
