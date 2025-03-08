# Copyright 2023 Accent Communications

from datetime import datetime, timedelta

from accent_dao.alchemy.stat_call_on_queue import StatCallOnQueue as StatCallOnQueueSchema
from accent_dao.tests.test_dao import DAOTestCase
from hamcrest import assert_that, contains_inanyorder, empty, has_property

from accent_purge_db.table_purger import StatCallOnQueuePurger


class TestStatCallOnQueuePurger(DAOTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def add_stat_call_on_queue(self, **kwargs):
        kwargs.setdefault('id', self._generate_int())
        kwargs.setdefault('time', datetime.now())
        kwargs.setdefault('callid', self._generate_int())
        kwargs.setdefault('ringtime', 0)
        kwargs.setdefault('talktime', 0)
        kwargs.setdefault('waittime', 0)
        kwargs.setdefault('status', 'answered')
        stat_call_on_queue = StatCallOnQueueSchema(**kwargs)
        self.add_me(stat_call_on_queue)
        return stat_call_on_queue.id

    def test_that_StatCallOnQueuePurger_keep_nothing_when_no_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep + 1))
        self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep + 2))
        self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep + 3))

        StatCallOnQueuePurger().purge(days_to_keep, self.session)

        result = self.session.query(StatCallOnQueueSchema).all()

        assert_that(result, empty())

    def test_that_StatCallOnQueuePurger_keep_everything_when_no_old_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        id_entry0 = self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep - 1))
        id_entry1 = self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep - 3))

        StatCallOnQueuePurger().purge(days_to_keep, self.session)

        result = self.session.query(StatCallOnQueueSchema).all()

        assert_that(
            result,
            contains_inanyorder(
                has_property('id', id_entry0),
                has_property('id', id_entry1),
                has_property('id', id_entry2),
            ),
        )

    def test_that_StatCallOnQueuePurger_keep_only_recent_entry(self):
        days_to_keep = 90
        current_time = datetime.now()

        self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep + 1))
        id_entry1 = self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep - 2))
        id_entry2 = self.add_stat_call_on_queue(time=current_time - timedelta(days=days_to_keep - 3))

        StatCallOnQueuePurger().purge(days_to_keep, self.session)

        result = self.session.query(StatCallOnQueueSchema).all()

        assert_that(
            result,
            contains_inanyorder(has_property('id', id_entry1), has_property('id', id_entry2)),
        )

    def test_that_StatCallOnQueuePurger_do_nothing_when_no_entry(self):
        days_to_keep = 90
        StatCallOnQueuePurger().purge(days_to_keep, self.session)

        result = self.session.query(StatCallOnQueueSchema).all()

        assert_that(result, empty())
