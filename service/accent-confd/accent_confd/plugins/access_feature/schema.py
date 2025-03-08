# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Length, OneOf

from accent_confd.helpers.mallow import BaseSchema, Link, ListLink


class AccessFeatureSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    host = fields.String(validate=Length(max=255))
    feature = fields.String(validate=OneOf(['phonebook']))
    enabled = fields.Boolean()
    links = ListLink(Link('access_features'))
