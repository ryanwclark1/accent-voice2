# Copyright 2023 Accent Communications

from datetime import datetime as dt
from datetime import timedelta
from pytz import UTC

from sqlalchemy import func

from accent_dao import stat_queue_periodic_dao
from accent_dao.alchemy.stat_queue_periodic import StatQueuePeriodic
from accent_dao.alchemy.stat_queue import StatQueue
from accent_dao.helpers.db_utils import flush_session
from .test_dao import DAOTestCase


class TestStatQueuePeriodicDAO(DAOTestCase):

    def _insert_queue_to_stat_queue(self, tenant_uuid=None):
        queue = StatQueue()
        queue.name = 'test_queue'
        queue.tenant_uuid = tenant_uuid or self.default_tenant.uuid

        self.add_me(queue)

        return queue.name, queue.id

    def _get_stats_for_queue(self):
        queue_name, queue_id = self._insert_queue_to_stat_queue()
        stats = {
            queue_id: {
                'abandoned': 7,
                'answered': 27,
                'closed': 5,
                'full': 4,
                'joinempty': 2,
                'leaveempty': 11,
                'timeout': 5,
                'divert_ca_ratio': 22,
                'divert_waittime': 15,
                'total': 98
            }
        }
        return stats

    def test_insert_periodic_stat(self):
        stats = self._get_stats_for_queue()
        period_start = dt(2012, 1, 1, 00, 00, 00, tzinfo=UTC)

        with flush_session(self.session):
            stat_queue_periodic_dao.insert_stats(self.session, stats, period_start)

        try:
            result = (self.session.query(StatQueuePeriodic)
                      .filter(StatQueuePeriodic.time == period_start)[0])

            self.assertEqual(result.abandoned, 7)
            self.assertEqual(result.answered, 27)
            self.assertEqual(result.closed, 5)
            self.assertEqual(result.full, 4)
            self.assertEqual(result.joinempty, 2)
            self.assertEqual(result.leaveempty, 11)
            self.assertEqual(result.timeout, 5)
            self.assertEqual(result.divert_ca_ratio, 22)
            self.assertEqual(result.divert_waittime, 15)
            self.assertEqual(result.total, 98)
        except LookupError:
            self.fail('Should have found a row')

    def test_get_most_recent_time(self):
        self.assertRaises(LookupError, stat_queue_periodic_dao.get_most_recent_time, self.session)

        stats = self._get_stats_for_queue()
        start = dt(2012, 1, 1, 00, 00, 00, tzinfo=UTC)

        with flush_session(self.session):
            for minute_increment in [-5, 5, 15, 22, 35, 65, 120]:
                delta = timedelta(minutes=minute_increment)
                time = start + delta
                stat_queue_periodic_dao.insert_stats(self.session, stats, time)

        result = stat_queue_periodic_dao.get_most_recent_time(self.session)
        expected = start + timedelta(minutes=120)

        self.assertEqual(result, expected)

    def test_clean_table(self):
        queue_name, queue_id = self._insert_queue_to_stat_queue()
        stats = {
            queue_id: {
                'full': 4,
                'total': 10
            }
        }
        period_start = dt(2012, 1, 1, 00, 00, 00, tzinfo=UTC)

        stat_queue_periodic_dao.insert_stats(self.session, stats, period_start)

        stat_queue_periodic_dao.clean_table(self.session)

        total = self.session.query(func.count(StatQueuePeriodic.time))[0][0]

        self.assertEqual(total, 0)

    def test_remove_after(self):
        queue_name, queue_id = self._insert_queue_to_stat_queue()
        stats = {
            queue_id: {
                'full': 4,
                'total': 10
            }
        }

        with flush_session(self.session):
            stat_queue_periodic_dao.insert_stats(self.session, stats, dt(2012, 1, 1, tzinfo=UTC))
            stat_queue_periodic_dao.insert_stats(self.session, stats, dt(2012, 1, 2, tzinfo=UTC))
            stat_queue_periodic_dao.insert_stats(self.session, stats, dt(2012, 1, 3, tzinfo=UTC))

        stat_queue_periodic_dao.remove_after(self.session, dt(2012, 1, 2, tzinfo=UTC))

        res = self.session.query(StatQueuePeriodic.time)

        self.assertEqual(res.count(), 1)
        self.assertEqual(res[0].time, dt(2012, 1, 1, tzinfo=UTC))
