# Copyright 2023 Accent Communications

from accent.mallow import fields, validate
from marshmallow import post_dump

from accent_auth.schemas import BaseSchema
from accent_auth.slug import Slug


class PolicyFullSchema(BaseSchema):
    uuid = fields.String(dump_only=True)
    tenant_uuid = fields.String(dump_only=True, attribute='tenant_uuid_exposed')
    name = fields.String(validate=validate.Length(min=1, max=80), required=True)
    slug = fields.String(
        validate=[validate.Length(min=1, max=80), validate.Regexp(Slug.valid_re())],
        missing=None,
    )
    description = fields.String(allow_none=True, missing=None)
    acl = fields.List(fields.String(), missing=[], attribute='acl')
    read_only = fields.Boolean(dump_only=True)
    shared = fields.Boolean(missing=False)

    @post_dump(pass_original=True)
    def set_shared_exposed_only_for_dump(self, data, original, **kwargs):
        data['shared'] = original.shared_exposed
        return data


class PolicyPutSchema(PolicyFullSchema):
    slug = fields.String(dump_only=True)
    shared = fields.String(dump_only=True)


policy_full_schema = PolicyFullSchema()
policy_put_schema = PolicyPutSchema()
