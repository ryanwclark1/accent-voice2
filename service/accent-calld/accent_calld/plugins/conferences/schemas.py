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
    muted = fields.Boolean()
    join_time = fields.Integer()
    admin = fields.Boolean()
    language = fields.String()
    call_id = fields.String()
    user_uuid = fields.String(allow_none=True)


participant_schema = ParticipantSchema()
