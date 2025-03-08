# Copyright 2023 Accent Communications

from accent_ui.helpers.extension import BaseConfdService


class SkillService(BaseConfdService):
    resource_confd = 'agent_skills'

    def __init__(self, confd_client):
        self._confd = confd_client
