# Copyright 2023 Accent Communications

from accent.mallow import fields
from marshmallow import EXCLUDE, Schema


class ParticipantSchema(Schema):
    class Meta:
        ordered = True
        unknown = EXCLUDE

    id = fields.String()
    caller_id_name = fields.String()
    caller_id_number = fields.String()
    call_id = fields.String()
    user_uuid = fields.String(allow_none=True)


class StatusSchema(Schema):
    class Meta:
        ordered = True
        unknown = EXCLUDE

    full = fields.Boolean()


participant_schema = ParticipantSchema()
status_schema = StatusSchema()
