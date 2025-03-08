# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Regexp

from accent_confd.helpers.mallow import BaseSchema, Link, ListLink
from accent_confd.helpers.validator import EXTEN_REGEX


class ExtensionFeatureSchema(BaseSchema):
    uuid = fields.UUID(dump_only=True)
    exten = fields.String(validate=Regexp(EXTEN_REGEX), required=True)
    context = fields.String(dump_only=True)
    feature = fields.String(dump_only=True)
    enabled = fields.Boolean()
    links = ListLink(Link('extensions_features', field='uuid'))
