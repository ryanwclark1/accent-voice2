# Copyright 2023 Accent Communications

from accent_dao.resources.schedule import dao as schedule_dao
from accent_dao.resources.user import dao as user_dao

from .resource import UserScheduleItem
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            UserScheduleItem,
            '/users/<int:user_id>/schedules/<int:schedule_id>',
            '/users/<uuid:user_id>/schedules/<int:schedule_id>',
            endpoint='user_schedules',
            resource_class_args=(service, user_dao, schedule_dao),
        )
