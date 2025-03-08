# Copyright 2023 Accent Communications

from hamcrest import assert_that, equal_to, none

from accent_dao.tests.test_dao import DAOTestCase


class TestAgentStatus(DAOTestCase):

    def test_agent_relationsip(self):
        agent = self.add_agent()
        agent_status = self.add_agent_login_status(agent_id=agent.id)

        self.session.expire_all()

        assert_that(agent_status.agent, equal_to(agent))

    def test_agent_relationsip_no_agent(self):
        agent_status = self.add_agent_login_status(agent_id=42)

        self.session.expire_all()

        assert_that(agent_status.agent, none())
