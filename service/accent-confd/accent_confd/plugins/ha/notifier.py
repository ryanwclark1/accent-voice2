# Copyright 2023 Accent Communications

from accent_bus.resources.ha.event import HAEditedEvent


class HANotifier:
    def __init__(self, bus, sysconfd):
        self.bus = bus
        self.sysconfd = sysconfd

    def edited(self, ha):
        event = HAEditedEvent()
        self.bus.queue_event(event)
        ha_sysconf = {
            'node_type': ha['node_type'],
            'remote_address': ha.get('remote_address') or '',
        }
        self.sysconfd.update_ha_config(ha_sysconf)
