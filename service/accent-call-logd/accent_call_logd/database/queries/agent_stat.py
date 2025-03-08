# Copyright 2023 Accent Communications

from accent_dao.alchemy.stat_agent import StatAgent
from accent_dao.alchemy.stat_agent_periodic import StatAgentPeriodic
from accent_dao.alchemy.stat_call_on_queue import StatCallOnQueue
from marshmallow import Schema, fields
from sqlalchemy import func, text

from .base import BaseDAO


class IntervalAsSeconds(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.total_seconds()


class StatRow(Schema):
    agent_id = fields.Integer()
    agent_number = fields.String()
    from_ = fields.DateTime(attribute='from', data_key='from')
    until = fields.DateTime()
    tenant_uuid = fields.UUID()
    answered = fields.Integer()
    conversation_time = fields.Integer()
    login_time = IntervalAsSeconds()
    pause_time = IntervalAsSeconds()
    wrapup_time = IntervalAsSeconds()


class StatAgentRow(Schema):
    agent_id = fields.Integer()
    number = fields.String()
    tenant_uuid = fields.UUID()


class AgentStatDAO(BaseDAO):
    def find_oldest_time(self, agent_id):
        with self.new_session() as session:
            query = (
                session.query(StatAgentPeriodic.time)
                .join(StatAgent)
                .filter(StatAgent.agent_id == agent_id)
                .filter(StatAgent.deleted.is_(False))
                .order_by(StatAgentPeriodic.time.asc())
                .limit(1)
            )
            return query.scalar()

    def get_stat_agents(self, tenant_uuids=None):
        with self.new_session() as session:
            query = session.query(
                StatAgent.agent_id, StatAgent.number, StatAgent.tenant_uuid
            ).filter(StatAgent.deleted.is_(False))
            query = self._add_tenant_filter(query, tenant_uuids)

            rows = query.all()
            results = []
            schema = StatAgentRow()
            for row in rows:
                results.append(schema.dump(row))
            return results

    def get_stat_agent(self, agent_id, tenant_uuids=None):
        with self.new_session() as session:
            query = (
                session.query(
                    StatAgent.agent_id, StatAgent.number, StatAgent.tenant_uuid
                )
                .filter(StatAgent.agent_id == agent_id)
                .filter(StatAgent.deleted.is_(False))
            )
            query = self._add_tenant_filter(query, tenant_uuids)

            row = query.first()
            if row:
                return StatAgentRow().dump(row)

    def get_interval(self, tenant_uuids, **filters):
        with self.new_session() as session:
            query = self._agent_stat_query(
                session, tenant_uuids=tenant_uuids, **filters
            )
            rows = query.all()
            results = []
            for row in rows:
                basic_stats = StatRow().dump(row)
                extra_stats = self._get_extra_stats(session, basic_stats, **filters)
                results.append({**basic_stats, **extra_stats})
        return results

    def get_interval_by_agent(self, tenant_uuids, agent_id, **filters):
        with self.new_session() as session:
            query = self._agent_stat_query(
                session, tenant_uuids=tenant_uuids, **filters
            )
            query = query.filter(StatAgent.agent_id == agent_id)
            row = query.first()
            result = None
            if row:
                basic_stats = StatRow().dump(row)
                extra_stats = self._get_extra_stats(session, basic_stats, **filters)
                result = {**basic_stats, **extra_stats}
        return result

    def _extract_timezone_to_postgres_format(self, from_):
        tz_offset = from_.strftime('%z') or '+0000'
        return f'{tz_offset[0:3]}:{tz_offset[3:]}'

    def _agent_stat_query(self, session, **filters):
        query = (
            session.query(
                func.min(StatAgent.agent_id).label('agent_id'),
                func.min(StatAgent.number).label('agent_number'),
                func.min(StatAgentPeriodic.time).label('from'),
                func.max(StatAgentPeriodic.time).label('until'),
                func.min(StatAgent.tenant_uuid).label('tenant_uuid'),
                func.sum(StatAgentPeriodic.login_time).label('login_time'),
                func.sum(StatAgentPeriodic.pause_time).label('pause_time'),
                func.sum(StatAgentPeriodic.wrapup_time).label('wrapup_time'),
            )
            .select_from(StatAgent)
            .filter(StatAgent.deleted.is_(False))
            .join(StatAgentPeriodic)
            .group_by(StatAgentPeriodic.stat_agent_id)
        )
        query = self._add_interval_query(StatAgentPeriodic, query, **filters)
        return query

    def _add_tenant_filter(self, query, tenant_uuids):
        if tenant_uuids:
            query = query.filter(StatAgent.tenant_uuid.in_(tenant_uuids))
        elif not tenant_uuids and tenant_uuids is not None:
            query = query.filter(text('false'))
        return query

    # NOTE: This only work because tables used have same column name
    def _add_interval_query(
        self,
        table,
        query,
        tenant_uuids=None,
        week_days=None,
        start_time=None,
        end_time=None,
        from_=None,
        until=None,
        timezone=None,
        **ignored,
    ):
        query = self._add_tenant_filter(query, tenant_uuids)

        if from_:
            query = query.filter(table.time >= from_)

        if until:
            query = query.filter(table.time < until)

        if timezone:
            timezone_name = str(timezone)
        else:
            timezone_name = 'UTC'

        if start_time is not None and end_time is not None:
            hour = func.extract('HOUR', table.time.op('AT TIME ZONE')(timezone_name))
            query = query.filter(hour.between(start_time, end_time))

        if week_days is not None:
            day_of_week = func.extract(
                'ISODOW', table.time.op('AT TIME ZONE')(timezone_name)
            )
            query = query.filter(day_of_week.in_(week_days))
        elif not week_days and week_days is not None:
            query = query.filter(text('false'))

        return query

    def _get_extra_stats(self, session, stats, **filters):
        answered, talk_time = self._get_answered_and_talk_time(
            session, stats['agent_id'], **filters
        )

        return {'answered': answered, 'conversation_time': talk_time}

    def _get_answered_and_talk_time(self, session, agent_id, **filters):
        query = (
            session.query(
                func.count(StatCallOnQueue.id),
                func.coalesce(func.sum(StatCallOnQueue.talktime), 0),
            )
            .filter(StatAgent.agent_id == agent_id)
            .filter(StatCallOnQueue.status == 'answered')
            .join(StatAgent)
        )
        query = self._add_interval_query(StatCallOnQueue, query, **filters)
        return query.first() or (0, 0)
