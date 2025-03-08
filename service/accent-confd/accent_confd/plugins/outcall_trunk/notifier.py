# Copyright 2023 Accent Communications

from accent_bus.resources.outcall_trunk.event import OutcallTrunksAssociatedEvent

from accent_confd import bus


class OutcallTrunkNotifier:
    def __init__(self, bus):
        self.bus = bus

    def associated_all_trunks(self, outcall, trunks):
        trunk_ids = [trunk.id for trunk in trunks]
        event = OutcallTrunksAssociatedEvent(outcall.id, trunk_ids, outcall.tenant_uuid)
        self.bus.queue_event(event)


def build_notifier():
    return OutcallTrunkNotifier(bus)
