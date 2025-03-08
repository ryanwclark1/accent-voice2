# Copyright 2023 Accent Communications

from accent_ui.helpers.extension import BaseConfdService


class SkillRuleService(BaseConfdService):
    resource_confd = 'queue_skill_rules'

    def __init__(self, confd_client):
        self._confd = confd_client
