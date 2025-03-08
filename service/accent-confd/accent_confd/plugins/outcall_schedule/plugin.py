# Copyright 2023 Accent Communications

from accent_dao.resources.outcall import dao as outcall_dao
from accent_dao.resources.schedule import dao as schedule_dao

from .resource import OutcallScheduleItem
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            OutcallScheduleItem,
            '/outcalls/<int:outcall_id>/schedules/<int:schedule_id>',
            endpoint='outcall_schedules',
            resource_class_args=(service, outcall_dao, schedule_dao),
        )
