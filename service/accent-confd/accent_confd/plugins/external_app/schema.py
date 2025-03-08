# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Length

from accent_confd.helpers.mallow import BaseSchema, Link, ListLink


class ExternalAppSchema(BaseSchema):
    tenant_uuid = fields.String(dump_only=True)
    name = fields.String(dump_only=True)
    label = fields.String(validate=Length(max=256), allow_none=True)
    configuration = fields.Dict(allow_none=True)

    links = ListLink(Link('external_apps', field='name'))


class ExternalAppNameSchema(BaseSchema):
    name = fields.String(validate=Length(max=128))
