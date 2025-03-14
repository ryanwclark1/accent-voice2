# Copyright 2023 Accent Communications

from accent.mallow import fields, validate
from marshmallow import ValidationError, validates_schema

from accent_auth.schemas import BaseSchema


class PasswordResetPostParameters(BaseSchema):
    password = fields.String(
        validate=validate.Length(min=1), required=True, allow_none=True
    )


class PasswordResetQueryParameters(BaseSchema):
    username = fields.String(validate=validate.Length(min=1, max=256), missing=None)
    email_address = fields.Email(data_key='email', missing=None)
    login = fields.String(validate=validate.Length(min=1, max=256), missing=None)

    @validates_schema
    def validate_mutually_exclusive_fields(self, data, **kwargs):
        username = data.get('username')
        email = data.get('email_address')
        login = data.get('login')

        if (username, email, login).count(None) != 2:
            msg = '"username" or "email" or "login" should be used'
            raise ValidationError(msg)
