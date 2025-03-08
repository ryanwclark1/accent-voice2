# Copyright 2023 Accent Communications

from accent_dao.resources.group import dao as group_dao
from accent_dao.resources.schedule import dao as schedule_dao

from .resource import GroupScheduleItem
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            GroupScheduleItem,
            '/groups/<int:group_uuid>/schedules/<int:schedule_id>',
            '/groups/<uuid:group_uuid>/schedules/<int:schedule_id>',
            endpoint='group_schedules',
            resource_class_args=(service, group_dao, schedule_dao),
        )
