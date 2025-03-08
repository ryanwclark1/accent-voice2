# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Length, Regexp

from accent_confd.helpers.mallow import BaseSchema
from accent_confd.plugins.user.schema import PASSWORD_REGEX, USERNAME_REGEX


class AccentUserSchema(BaseSchema):
    uuid = fields.String()
    firstname = fields.String(validate=Length(max=128), required=True)
    lastname = fields.String(validate=Length(max=128), allow_none=True)
    email_address = fields.String(validate=Length(max=254), allow_none=True)
    username = fields.String(validate=Regexp(USERNAME_REGEX), allow_none=True)
    password = fields.String(validate=Regexp(PASSWORD_REGEX), allow_none=True)
    enabled = fields.Boolean(allow_none=True)
