# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow.validate import Length, OneOf, Range

from accent_auth.schemas import BaseSchema


class LDAPConfig(BaseSchema):
    tenant_uuid = fields.String(dump_only=True, default=None)
    host = fields.String(validate=Length(max=512), required=True, default=None)
    port = fields.Integer(required=True, default=None)
    protocol_version = fields.Integer(
        validate=Range(min=2, max=3), missing=3, default=None
    )
    protocol_security = fields.String(
        validate=OneOf(['ldaps', 'tls']),
        allow_none=True,
        default=None,
    )
    bind_dn = fields.String(validate=Length(max=256), allow_none=True, default=None)
    user_base_dn = fields.String(validate=Length(max=256), required=True, default=None)
    user_login_attribute = fields.String(
        validate=Length(max=64), required=True, default=None
    )
    user_email_attribute = fields.String(
        validate=Length(max=64), required=True, default=None
    )
    search_filters = fields.String(allow_none=True, default=None)


class LDAPConfigEdit(LDAPConfig):
    bind_password = fields.String(load_only=True, allow_none=True)


ldap_config_schema = LDAPConfig()
ldap_config_edit_schema = LDAPConfigEdit()
