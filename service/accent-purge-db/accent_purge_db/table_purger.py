# Copyright 2023 Accent Communications

import abc
import datetime

from accent_dao.alchemy.cel import CEL
from accent_dao.alchemy.queue_log import QueueLog
from accent_dao.alchemy.stat_agent_periodic import StatAgentPeriodic
from accent_dao.alchemy.stat_call_on_queue import StatCallOnQueue
from accent_dao.alchemy.stat_queue_periodic import StatQueuePeriodic
from accent_dao.alchemy.stat_switchboard_queue import StatSwitchboardQueue
from sqlalchemy import func


class TablePurger(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def purge(self, days_to_keep, session):
        pass


class CELPurger(TablePurger):
    def purge(self, days_to_keep, session):
        query = CEL.__table__.delete().where(CEL.eventtime < (func.now() - datetime.timedelta(days=days_to_keep)))
        session.execute(query)


class QueueLogPurger(TablePurger):
    def purge(self, days_to_keep, session):
        query = QueueLog.__table__.delete().where(QueueLog.time < (func.now() - datetime.timedelta(days=days_to_keep)))
        session.execute(query)


class StatAgentPeriodicPurger(TablePurger):
    def purge(self, days_to_keep, session):
        query = StatAgentPeriodic.__table__.delete().where(
            StatAgentPeriodic.time < (func.now() - datetime.timedelta(days=days_to_keep))
        )
        session.execute(query)


class StatCallOnQueuePurger(TablePurger):
    def purge(self, days_to_keep, session):
        query = StatCallOnQueue.__table__.delete().where(
            StatCallOnQueue.time < (func.now() - datetime.timedelta(days=days_to_keep))
        )
        session.execute(query)


class StatQueuePeriodicPurger(TablePurger):
    def purge(self, days_to_keep, session):
        query = StatQueuePeriodic.__table__.delete().where(
            StatQueuePeriodic.time < (func.now() - datetime.timedelta(days=days_to_keep))
        )
        session.execute(query)


class StatSwitchboardPurger(TablePurger):
    def purge(self, days_to_keep, session):
        query = StatSwitchboardQueue.__table__.delete().where(
            StatSwitchboardQueue.time < (func.localtimestamp() - datetime.timedelta(days=days_to_keep))
        )
        session.execute(query)
