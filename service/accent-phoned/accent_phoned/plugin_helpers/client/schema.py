# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow_helpers import Schema


class UserUUIDSchema(Schema):
    accent_user_uuid = fields.String(required=True)


class LookupSchema(UserUUIDSchema):
    term = fields.String(required=True)
    limit = fields.Integer(missing=None)
    offset = fields.Integer(missing=0)
