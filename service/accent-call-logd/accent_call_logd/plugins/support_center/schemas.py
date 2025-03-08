# Copyright 2023 Accent Communications

from datetime import time

import pytz
from accent.mallow import fields
from accent.mallow.validate import ContainsOnly, OneOf, Range, Regexp
from accent.mallow_helpers import Schema
from marshmallow import ValidationError, post_load, pre_dump, pre_load, validates_schema

HOUR_REGEX = r"^([0,1][0-9]|2[0-3]):[0-5][0-9]$"


class _StatisticsPeriodSchema(Schema):
    from_ = fields.String(attribute='from', data_key='from')
    until = fields.String()
    tenant_uuid = fields.UUID(default=None)

    @pre_dump
    def convert_from_and_until_to_isoformat(self, data, **kwargs):
        if data.get('from'):
            data['from'] = data['from'].isoformat()
        if data.get('until'):
            data['until'] = data['until'].isoformat()
        return data


class AgentStatisticsSchema(_StatisticsPeriodSchema):
    agent_id = fields.Integer(default=None)
    agent_number = fields.String(default=None)
    answered = fields.Integer(default=0)
    conversation_time = fields.Integer(default=0)
    login_time = fields.Integer(default=0)
    pause_time = fields.Integer(default=0)
    wrapup_time = fields.Integer(default=0)


class AgentStatisticsSchemaList(Schema):
    items = fields.Nested(AgentStatisticsSchema, many=True)
    total = fields.Integer()


class QueueStatisticsSchema(_StatisticsPeriodSchema):
    queue_id = fields.Integer(default=None)
    queue_name = fields.String(default=None)
    received = fields.Integer(attribute='total', default=0)
    answered = fields.Integer(default=0)
    abandoned = fields.Integer(default=0)
    closed = fields.Integer(default=0)
    not_answered = fields.Integer(attribute='timeout', default=0)
    saturated = fields.Integer(default=0)
    blocked = fields.Integer(attribute='blocking', default=0)
    average_waiting_time = fields.Integer(default=None)
    answered_rate = fields.Float(default=None)
    quality_of_service = fields.Float(attribute='qos', default=None)


class _QoSSchema(Schema):
    min_ = fields.Integer(default=None, attribute='min', data_key='min')
    max_ = fields.Integer(default=None, attribute='max', data_key='max')
    answered = fields.Integer(default=0)
    abandoned = fields.Integer(default=0)


class QueueStatisticsQoSSchema(_StatisticsPeriodSchema):
    queue_id = fields.Integer(default=None)
    queue_name = fields.String(default=None)
    quality_of_service = fields.List(fields.Nested(_QoSSchema))


class _StatisticsListRequestSchema(Schema):
    from_ = fields.DateTime(data_key='from', missing=None)
    until = fields.DateTime(missing=None)
    day_start_time = fields.String(attribute='start_time', validate=Regexp(HOUR_REGEX))
    day_end_time = fields.String(attribute='end_time', validate=Regexp(HOUR_REGEX))
    week_days = fields.List(
        fields.Integer(),
        missing=[1, 2, 3, 4, 5, 6, 7],
        validate=ContainsOnly([1, 2, 3, 4, 5, 6, 7]),
    )
    timezone = fields.String(validate=OneOf(pytz.all_timezones), missing='UTC')

    def _normalize_datetime(self, dt, timezone):
        if not dt.tzinfo:
            return timezone.normalize(timezone.localize(dt))
        else:
            utc_dt = pytz.utc.normalize(dt)
            return timezone.normalize(utc_dt)

    @pre_load
    def convert_week_days_to_list(self, data, **kwargs):
        result = data.copy()
        if not isinstance(data, dict):
            result = data.to_dict()
        if data.get('week_days'):
            result['week_days'] = list(set(data['week_days'].split(',')))
        return result

    @post_load
    def convert_time_to_hour(self, data, **kwargs):
        if data.get('start_time'):
            start_time = time.fromisoformat(data['start_time'])
            data['start_time'] = start_time.hour
        if data.get('end_time'):
            end_time = time.fromisoformat(data['end_time'])
            data['end_time'] = end_time.hour
        return data

    @post_load
    def default_timezone_on_datetime(self, data, **kwargs):
        timezone = pytz.timezone(data.get('timezone'))
        from_ = data.get('from_')
        until = data.get('until')
        if from_:
            data['from_'] = self._normalize_datetime(from_, timezone)
        if until:
            data['until'] = self._normalize_datetime(until, timezone)
        return data

    @validates_schema
    def validate_dates(self, data, **kwargs):
        from_ = data.get('from_', None)
        until = data.get('until', None)
        timezone = pytz.timezone(data.get('timezone'))
        if from_:
            from_ = self._normalize_datetime(from_, timezone)
        if until:
            until = self._normalize_datetime(until, timezone)
        if from_ and until and until <= from_:
            raise ValidationError({'until': 'Field must be greater than from'})

    @validates_schema
    def validate_start_end_times(self, data, **kwargs):
        if data.get('start_time') and data.get('end_time'):
            if data['start_time'] >= data['end_time']:
                raise ValidationError(
                    {'day_start_time': 'Field must be lower than day_end_time'}
                )


class AgentStatisticsListRequestSchema(_StatisticsListRequestSchema):
    qos_threshold = fields.Integer(validate=Range(min=0))


class QueueStatisticsListRequestSchema(_StatisticsListRequestSchema):
    qos_threshold = fields.Integer(validate=Range(min=0))


class AgentStatisticsRequestSchema(AgentStatisticsListRequestSchema):
    interval = fields.String(validate=OneOf(['hour', 'day', 'month']))


class QueueStatisticsRequestSchema(QueueStatisticsListRequestSchema):
    interval = fields.String(validate=OneOf(['hour', 'day', 'month']))


class QueueStatisticsQoSRequestSchema(_StatisticsListRequestSchema):
    interval = fields.String(validate=OneOf(['hour', 'day', 'month']))
    qos_thresholds = fields.List(fields.Integer(validate=Range(min=0)), missing=[])

    @pre_load
    def convert_qos_thresholds_to_list(self, data, **kwargs):
        result = data.copy()
        if not isinstance(result, dict):
            result = result.to_dict()
        if data.get('qos_thresholds'):
            result['qos_thresholds'] = list(set(data['qos_thresholds'].split(',')))
        return result

    @post_load
    def sort_qos_thresholds(self, data, **kwargs):
        result = data.copy()
        if data.get('qos_thresholds'):
            result['qos_thresholds'] = sorted(data['qos_thresholds'])
        return result


class QueueStatisticsSchemaList(Schema):
    items = fields.Nested(QueueStatisticsSchema, many=True)
    total = fields.Integer()


class QueueStatisticsQoSSchemaList(Schema):
    items = fields.Nested(QueueStatisticsQoSSchema, many=True)
    total = fields.Integer()
