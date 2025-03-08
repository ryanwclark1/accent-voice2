# Copyright 2023 Accent Communications

from accent.mallow import fields

from accent_auth.schemas import BaseSchema


class IDPUserSchema(BaseSchema):
    uuid = fields.String(required=True)


class IDPUsersSchema(BaseSchema):
    users = fields.Nested(IDPUserSchema, many=True, required=True)
