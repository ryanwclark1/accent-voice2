# Copyright 2023 Accent Communications

from accent.mallow import fields, validate

from accent_auth.schemas import BaseSchema


class UserRegisterPostSchema(BaseSchema):
    username = fields.String(validate=validate.Length(min=1, max=256))
    password = fields.String(validate=validate.Length(min=1), required=True)
    firstname = fields.String(missing=None)
    lastname = fields.String(missing=None)
    email_address = fields.Email(required=True)
    purpose = fields.Constant('user')
    authentication_method = fields.Constant('default')
