# Copyright 2023 Accent Communications


class MockEvent:
    def __init__(self, name, routing_key=None, required_acl=None, **kwargs) -> None:
        self.name = name
        self.routing_key = routing_key
        self.required_acl = required_acl
        self._body = kwargs

    def marshal(self):
        return dict(self._body.items())
