# Copyright 2023 Accent Communications

from .resource import VoicemailZoneMessagesList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            VoicemailZoneMessagesList,
            '/asterisk/voicemail/zonemessages',
            resource_class_args=(service,),
        )
