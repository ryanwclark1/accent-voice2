# Copyright 2023 Accent Communications

from marshmallow import Schema, fields


class QueuedCallSchema(Schema):
    id = fields.String(attribute='id')
    caller_id_name = fields.String()
    caller_id_number = fields.String()


queued_call_schema = QueuedCallSchema()


class HeldCallSchema(Schema):
    id = fields.String(attribute='id')
    caller_id_name = fields.String()
    caller_id_number = fields.String()


held_call_schema = HeldCallSchema()


class AnswerCallSchema(Schema):
    line_id = fields.Integer(missing=None)


answer_call_schema = AnswerCallSchema()
