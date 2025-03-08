# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Length, OneOf

from accent_confd.helpers.mallow import BaseSchema


class GETQueryStringSchema(BaseSchema):
    view = fields.String(validate=OneOf(['fallback']), missing=None)


class UserExternalAppSchema(BaseSchema):
    name = fields.String(dump_only=True)
    label = fields.String(validate=Length(max=256), allow_none=True)
    configuration = fields.Dict(allow_none=True)


class UserExternalAppNameSchema(BaseSchema):
    name = fields.String(validate=Length(max=128))
