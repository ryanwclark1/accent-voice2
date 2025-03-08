# Copyright 2023 Accent Communications

from marshmallow import fields
from marshmallow.validate import Length

from accent_confd.helpers.mallow import BaseSchema, PJSIPSection, PJSIPSectionOption


class PJSIPTransportDeleteRequestSchema(BaseSchema):
    fallback = fields.UUID(missing=None)


class PJSIPTransportSchema(BaseSchema):
    uuid = fields.UUID(dump_only=True)
    name = fields.String(validate=PJSIPSection(), required=True)
    options = fields.List(
        PJSIPSectionOption(),
        validate=Length(max=128),
        missing=[],
    )
