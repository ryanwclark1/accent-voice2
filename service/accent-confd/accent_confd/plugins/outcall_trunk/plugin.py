# Copyright 2023 Accent Communications

from accent_dao.resources.outcall import dao as outcall_dao
from accent_dao.resources.trunk import dao as trunk_dao

from .resource import OutcallTrunkList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            OutcallTrunkList,
            '/outcalls/<int:outcall_id>/trunks',
            resource_class_args=(service, outcall_dao, trunk_dao),
        )
