# Copyright 2023 Accent Communications

from . import http


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        session_service = dependencies['session_service']

        api.add_resource(
            http.Sessions,
            '/sessions',
            resource_class_args=[session_service],
        )
        api.add_resource(
            http.Session,
            '/sessions/<uuid:session_uuid>',
            resource_class_args=[session_service],
        )
