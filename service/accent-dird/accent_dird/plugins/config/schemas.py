
from accent.mallow import fields
from marshmallow import Schema
from marshmallow.validate import Equal


class ConfigPatchSchema(Schema):
    op = fields.String(validate=Equal('replace'))
    path = fields.String(validate=Equal('/debug'))
    value = fields.Boolean()


config_patch_schema = ConfigPatchSchema()