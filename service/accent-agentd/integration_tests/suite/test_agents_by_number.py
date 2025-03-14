# Copyright 2023 Accent Communications

from accent_test_helpers import until
from hamcrest import all_of, assert_that, contains, has_entries, has_key

from .helpers import fixtures
from .helpers.base import BaseIntegrationTest


class TestAgentsByNumber(BaseIntegrationTest):
    asset = 'base'

    @fixtures.user_line_extension(exten='1001', context='default')
    @fixtures.agent(number='1001')
    def test_event_on_login(self, user_line_extension, agent):
        event_accumulator = self.bus.accumulator(
            headers={'name': 'agent_status_update'}
        )

        self.agentd.agents.login_agent_by_number(
            agent['number'],
            user_line_extension['exten'],
            user_line_extension['context'],
        )

        def event_received():
            events = event_accumulator.accumulate(with_headers=True)
            assert_that(
                events,
                contains(
                    has_entries(
                        message=has_entries(
                            data=has_entries(agent_id=agent['id'], status='logged_in')
                        ),
                        headers=all_of(
                            has_key('tenant_uuid'),
                        ),
                    )
                ),
            ),

        until.assert_(event_received, tries=3)
