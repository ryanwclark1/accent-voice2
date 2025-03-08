# Copyright 2023 Accent Communications

from marshmallow import fields

from accent_confd.helpers.mallow import BaseSchema


class TenantSchema(BaseSchema):
    uuid = fields.UUID(dump_only=True)
    sip_templates_generated = fields.Boolean(dump_only=True)
    global_sip_template_uuid = fields.UUID(dump_only=True)
    webrtc_sip_template_uuid = fields.UUID(dump_only=True)
    registration_trunk_sip_template_uuid = fields.UUID(dump_only=True)
    meeting_guest_sip_template_uuid = fields.UUID(dump_only=True)
