# Copyright 2023 Accent Communications

from accent_dao.resources.line import dao as line_dao
from accent_dao.resources.user import dao as user_dao

from .resource import UserLineAssociatedEndpointSipItem


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']

        api.add_resource(
            UserLineAssociatedEndpointSipItem,
            '/users/<uuid:user_uuid>/lines/<line_id>/associated/endpoints/sip',
            resource_class_args=(user_dao, line_dao),
        )
