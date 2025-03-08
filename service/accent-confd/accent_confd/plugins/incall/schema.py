# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Length, OneOf

from accent_confd.helpers.destination import DestinationField
from accent_confd.helpers.mallow import BaseSchema, Link, ListLink, Nested


class IncallSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    tenant_uuid = fields.String(dump_only=True)
    preprocess_subroutine = fields.String(validate=Length(max=79), allow_none=True)
    greeting_sound = fields.String(validate=Length(max=255), allow_none=True)
    caller_id_mode = fields.String(
        validate=OneOf(['prepend', 'overwrite', 'append']), allow_none=True
    )
    caller_id_name = fields.String(validate=Length(max=80), allow_none=True)
    description = fields.String(allow_none=True)
    destination = DestinationField(required=True)
    links = ListLink(Link('incalls'))

    extensions = Nested(
        'ExtensionSchema',
        only=['id', 'exten', 'context', 'links'],
        many=True,
        dump_only=True,
    )
    schedules = Nested(
        'ScheduleSchema', only=['id', 'name', 'links'], many=True, dump_only=True
    )
