# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow.validate import Length

from accent_auth import schemas


class MicrosoftSchema(schemas.BaseSchema):
    scope = fields.List(fields.String(validate=Length(min=1, max=512)))
    access_token = fields.String(dump_only=True)
    token_expiration = fields.Integer(dump_only=True)
