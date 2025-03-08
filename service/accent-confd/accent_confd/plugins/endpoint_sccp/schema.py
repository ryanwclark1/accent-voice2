# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Length

from accent_confd.helpers.mallow import BaseSchema, Link, ListLink, Nested


class SccpSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    tenant_uuid = fields.String(dump_only=True)
    options = fields.List(fields.List(fields.String(), validate=Length(equal=2)))
    links = ListLink(Link('endpoint_sccp'))

    line = Nested('LineSchema', only=['id', 'links'], dump_only=True)
