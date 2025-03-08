# Copyright 2023 Accent Communications

from accent_dao.resources.user import dao as user_dao

from .resource import UserCallerIDList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']

        service = build_service()

        api.add_resource(
            UserCallerIDList,
            '/users/<uuid:user_id>/callerids/outgoing',
            '/users/<int:user_id>/callerids/outgoing',
            resource_class_args=(service, user_dao),
        )
