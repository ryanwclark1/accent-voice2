# Copyright 2023 Accent Communications

from accent_dao.resources.extension import dao as extension_dao
from accent_dao.resources.outcall import dao as outcall_dao

from .resource import OutcallExtensionItem
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            OutcallExtensionItem,
            '/outcalls/<int:outcall_id>/extensions/<int:extension_id>',
            endpoint='outcall_extensions',
            resource_class_args=(service, outcall_dao, extension_dao),
        )
