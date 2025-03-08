# Copyright 2023 Accent Communications

from marshmallow import Schema, fields
from marshmallow.validate import Length


class AdhocConferenceCreationSchema(Schema):
    host_call_id = fields.Str(validate=Length(min=1), required=True)
    participant_call_ids = fields.List(
        fields.Str(validate=Length(min=1), required=True)
    )


adhoc_conference_creation_schema = AdhocConferenceCreationSchema()
