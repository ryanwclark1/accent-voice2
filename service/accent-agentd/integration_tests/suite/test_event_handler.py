# Copyright 2023 Accent Communications

import time

from accent_test_helpers import until
from hamcrest import assert_that, is_

from .helpers import fixtures
from .helpers.base import BaseIntegrationTest


class TestEventHandler(BaseIntegrationTest):
    asset = 'base'

    @fixtures.user_line_extension(exten='1001', context='default')
    @fixtures.agent(number='1001')
    @fixtures.queue()
    def test_delete_queue_event(self, user_line_extension, agent, queue):
        with self.database.queries() as queries:
            queries.associate_user_agent(user_line_extension['user_id'], agent['id'])
            queries.associate_queue_agent(queue['id'], agent['id'])
            queries.insert_agent_membership_status(queue['id'], agent['id'])

        def test_on_msg_received():
            self.bus.send_delete_queue_event(queue['id'])
            time.sleep(0.5)

            with self.database.queries() as queries:
                membership = queries.get_agent_membership_status(
                    queue['id'], agent['id']
                )
                assert_that(membership, is_(None))

        until.assert_(test_on_msg_received, tries=10)
