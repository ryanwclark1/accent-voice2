# Copyright 2023 Accent Communications

from ..common.event import ServiceEvent


class AMIEvent(ServiceEvent):
    service = 'amid'
    name = '{ami_event}'
    routing_key_fmt = 'ami.{name}'

    def __init__(self, ami_event: str, variables: dict[str, str]):
        self.name = type(self).name.format(ami_event=ami_event)
        super().__init__(variables)
