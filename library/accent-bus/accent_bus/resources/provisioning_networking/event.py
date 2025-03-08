# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class ProvisioningNetworkingEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'provisioning_networking_edited'
    routing_key_fmt = 'config.provisioning.networking.edited'

    def __init__(self) -> None:
        super().__init__()
