# Copyright 2023 Accent Communications

from .http import SetupResource
from .services import SetupService


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = SetupService(dependencies['config'], dependencies['stopper'])
        api.add_resource(SetupResource, '/setup', resource_class_args=[service])
