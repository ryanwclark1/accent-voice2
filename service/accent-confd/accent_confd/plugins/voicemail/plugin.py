# Copyright 2023 Accent Communications

from .middleware import VoicemailMiddleWare
from .resource import VoicemailItem, VoicemailList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()
        middleware_handle = dependencies['middleware_handle']

        middleware = VoicemailMiddleWare(service)
        middleware_handle.register('voicemail', middleware)

        api.add_resource(
            VoicemailList,
            '/voicemails',
            resource_class_args=(service, middleware),
        )

        api.add_resource(
            VoicemailItem,
            '/voicemails/<int:id>',
            endpoint='voicemails',
            resource_class_args=(service, middleware),
        )
