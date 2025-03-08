# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class LiveReloadEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'live_reload_edited'
    routing_key_fmt = 'config.live_reload.edited'

    def __init__(self, live_reload_enabled: bool):
        content = {'live_reload_enabled': live_reload_enabled}
        super().__init__(content)
