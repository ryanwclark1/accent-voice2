# Copyright 2023 Accent Communications

from .resource import SkillRuleItem, SkillRuleList
from .service import build_service


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']
        service = build_service()

        api.add_resource(
            SkillRuleList, '/queues/skillrules', resource_class_args=(service,)
        )

        api.add_resource(
            SkillRuleItem,
            '/queues/skillrules/<int:id>',
            endpoint='skillrules',
            resource_class_args=(service,),
        )
