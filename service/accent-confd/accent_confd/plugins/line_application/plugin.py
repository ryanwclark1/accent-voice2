# Copyright 2023 Accent Communications

from accent_dao.resources.application import dao as application_dao
from accent_dao.resources.line import dao as line_dao

from .resource import LineApplicationAssociation
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()
        api.add_resource(
            LineApplicationAssociation,
            '/lines/<int:line_id>/applications/<uuid:application_uuid>',
            endpoint='line_applications',
            resource_class_args=(line_dao, application_dao, service),
        )
