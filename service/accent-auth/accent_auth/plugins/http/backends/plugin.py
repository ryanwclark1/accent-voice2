# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        args = (dependencies['config'],)

        api.add_resource(
            http.Backends,
            '/backends',
            resource_class_args=args,
        )
