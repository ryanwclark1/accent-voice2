# Copyright 2023 Accent Communications


class MiddleWareHandle:
    def __init__(self):
        self._middlewares = {}

    def register(self, resource_name, middleware):
        self._middlewares[resource_name] = middleware

    def get(self, resource_name):
        return self._middlewares[resource_name]
