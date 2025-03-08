# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow.validate import Length

from accent_auth.schemas import BaseSchema


class SamlConfig(BaseSchema):
    domain_uuid = fields.String(validate=Length(min=36, max=38), required=True)
    entity_id = fields.String(validate=Length(min=1, max=512), required=True)
    tenant_uuid = fields.String(validate=Length(min=36, max=38), required=False)
    acs_url = fields.String(validate=Length(min=1, max=512), required=True)


class SamlConfigWithMetadata(SamlConfig):
    idp_metadata = fields.String(required=True)


saml_config_schema = SamlConfig()


class SamlAcsUrlTemplate(BaseSchema):
    acs_url = fields.String(validate=Length(min=1, max=512), required=True)


saml_acs_url_template_schema = SamlAcsUrlTemplate()
