# Copyright 2023 Accent Communications

from accent.mallow import fields
from marshmallow import Schema
from marshmallow.validate import Equal, OneOf


class ConfigPatchSchema(Schema):
    op = fields.String(validate=Equal('replace'))
    path = fields.String(validate=OneOf(['/debug', '/profiling_enabled']))
    value = fields.Boolean()


config_patch_schema = ConfigPatchSchema()
