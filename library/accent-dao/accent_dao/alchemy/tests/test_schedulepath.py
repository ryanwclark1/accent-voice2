# Copyright 2023 Accent Communications

from hamcrest import (
    assert_that,
    equal_to,
)

from accent_dao.tests.test_dao import DAOTestCase

from ..schedule import Schedule


class TestSchedule(DAOTestCase):

    def test_getter(self):
        schedule = self.add_schedule()
        schedule_path = self.add_schedule_path(schedule_id=schedule.id)

        self.session.expire_all()
        assert_that(schedule_path.schedule, equal_to(schedule))

    def test_creator(self):
        schedule = Schedule(tenant_uuid=self.default_tenant.uuid)
        schedule_path = self.add_schedule_path(schedule=schedule)

        self.session.expire_all()
        assert_that(schedule_path.schedule_id, equal_to(schedule.id))
