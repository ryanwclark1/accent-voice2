# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow_helpers import Schema


class ExportSchema(Schema):
    uuid = fields.UUID()
    tenant_uuid = fields.UUID()
    user_uuid = fields.UUID()
    requested_at = fields.DateTime()
    filename = fields.String()
    status = fields.String()
