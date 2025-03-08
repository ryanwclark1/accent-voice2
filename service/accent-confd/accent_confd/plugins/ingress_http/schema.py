# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Length, OneOf

from accent_confd.helpers.mallow import BaseSchema, Link, ListLink


class IngressHTTPSchema(BaseSchema):
    uuid = fields.UUID(dump_only=True)
    tenant_uuid = fields.UUID(dump_only=True)
    uri = fields.String(validate=Length(min=1, max=1024), required=True)

    links = ListLink(Link('ingresses_http', field='uuid'))


class IngressViewSchema(BaseSchema):
    view = fields.String(validate=OneOf(['fallback', 'default']), missing=None)
