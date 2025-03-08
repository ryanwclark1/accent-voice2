# Copyright 2023 Accent Communications

from accent.mallow import fields, validate

from accent_auth.schemas import DOMAIN_RE, BaseSchema


class SAMLSSOSchema(BaseSchema):
    redirect_url = fields.String(validate=validate.Length(min=1))
    domain = fields.String(validate=validate.Regexp(DOMAIN_RE))
