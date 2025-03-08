# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Length

from accent_confd.helpers.mallow import BaseSchema


class ProvisioningNetworkingSchema(BaseSchema):
    provision_host = fields.String(
        validate=Length(max=39), attribute='net4_ip', allow_none=True
    )
    provision_http_port = fields.Integer(attribute='http_port')
    provision_http_base_url = fields.String(
        validate=Length(max=255), attribute='http_base_url', allow_none=True
    )
