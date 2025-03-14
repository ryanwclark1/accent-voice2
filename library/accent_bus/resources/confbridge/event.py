# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class ConfBridgeAccentDefaultBridgeEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'confbridge_accent_default_bridge_edited'
    routing_key_fmt = 'config.confbridge_accent_default_bridge.edited'

    def __init__(self) -> None:
        super().__init__()


class ConfBridgeAccentDefaultUserEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'confbridge_accent_default_user_edited'
    routing_key_fmt = 'config.confbridge_accent_default_user.edited'

    def __init__(self) -> None:
        super().__init__()
