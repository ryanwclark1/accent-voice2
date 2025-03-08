# Copyright 2023 Accent Communications

from marshmallow import fields

from accent_confd.helpers.mallow import BaseSchema


class UserCallerIDSchema(BaseSchema):
    number = fields.String(dump_only=True)
    type = fields.String(dump_only=True)
