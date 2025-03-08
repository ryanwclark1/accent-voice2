# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow_helpers import Schema


class LookupGigasetSchema(Schema):
    set_first = fields.String(attribute='term', missing='')
    count = fields.Integer(attribute='limit', missing=None)
    first = fields.Integer(attribute='offset', missing=1)
