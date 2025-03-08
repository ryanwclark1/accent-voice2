# Copyright 2023 Accent Communications

from accent_dao.resources.conference import dao as conference_dao
from accent_dao.resources.extension import dao as extension_dao

from .resource import ConferenceExtensionItem
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            ConferenceExtensionItem,
            '/conferences/<int:conference_id>/extensions/<int:extension_id>',
            endpoint='conference_extensions',
            resource_class_args=(service, conference_dao, extension_dao),
        )
