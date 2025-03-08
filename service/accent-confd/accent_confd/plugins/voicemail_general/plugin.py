# Copyright 2023 Accent Communications

from .resource import VoicemailGeneralList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            VoicemailGeneralList,
            '/asterisk/voicemail/general',
            resource_class_args=(service,),
        )
