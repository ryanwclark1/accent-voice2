# Copyright 2023 Accent Communications

from datetime import datetime, timedelta

from accent_dao.alchemy.stat_queue_periodic import (
    StatQueuePeriodic as StatQueuePeriodicSchema,
)
from accent_dao.tests.test_dao import DAOTestCase
from hamcrest import assert_that, contains_inanyorder, empty, has_property

from accent_purge_db.table_purger import StatQueuePeriodicPurger


class TestStatQueuePeriodicPurger(DAOTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def add_stat_queue_periodic(self, **kwargs):
        kwargs.setdefault('id', self._generate_int())
        kwargs.setdefault('time', datetime.now())
        kwargs.setdefault('answered', 0)
        kwargs.setdefault('abandoned', 0)
        kwargs.setdefault('total', 0)
        kwargs.setdefault('full', 0)
        kwargs.setdefault('closed', 0)
        kwargs.setdefault('joinempty', 0)
        kwargs.setdefault('leaveempty', 0)
        kwargs.setdefault('divert_ca_ratio', 0)
        kwargs.setdefault('divert_waittime', 0)
        kwargs.setdefault('timeout', 0)
        stat_queue_periodic = StatQueuePeriodicSchema(**kwargs)
        self.add_me(stat_queue_periodic)
        return stat_queue_periodic.id

    def test_that_StatQueuePeriodicPurger_keep_nothing_when_no_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep + 1))
        self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep + 2))
        self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep + 3))

        StatQueuePeriodicPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatQueuePeriodicSchema).all()

        assert_that(result, empty())

    def test_that_StatQueuePeriodicPurger_keep_everything_when_no_old_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        id_entry0 = self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep - 1))
        id_entry1 = self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep - 3))

        StatQueuePeriodicPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatQueuePeriodicSchema).all()

        assert_that(
            result,
            contains_inanyorder(
                has_property('id', id_entry0),
                has_property('id', id_entry1),
                has_property('id', id_entry2),
            ),
        )

    def test_that_StatQueuePeriodicPurger_keep_only_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep + 1))
        id_entry1 = self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_stat_queue_periodic(time=current_time - timedelta(days=days_to_keep - 3))

        StatQueuePeriodicPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatQueuePeriodicSchema).all()

        assert_that(
            result,
            contains_inanyorder(has_property('id', id_entry1), has_property('id', id_entry2)),
        )

    def test_that_StatQueuePeriodicPurger_do_nothing_when_no_entry(self):
        days_to_keep = 90
        StatQueuePeriodicPurger().purge(days_to_keep, self.session)

        result = self.session.query(StatQueuePeriodicSchema).all()

        assert_that(result, empty())
