# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow_helpers import Schema
from marshmallow import post_load


class FaxCreationRequestSchema(Schema):
    context = fields.String(required=True)
    extension = fields.String(required=True)
    caller_id = fields.String(missing='Accent Fax')
    ivr_extension = fields.String(missing=None)
    wait_time = fields.Integer(missing=None)

    @post_load
    def remove_extension_whitespace(self, call_request, **kwargs):
        call_request['extension'] = ''.join(call_request['extension'].split())
        return call_request


class UserFaxCreationRequestSchema(Schema):
    extension = fields.String(required=True)
    caller_id = fields.String(missing='Accent Fax')
    ivr_extension = fields.String(missing=None)
    wait_time = fields.Integer(missing=None)

    @post_load
    def remove_extension_whitespace(self, call_request, **kwargs):
        call_request['extension'] = ''.join(call_request['extension'].split())
        return call_request


class FaxSchema(Schema):
    id = fields.String(dump_only=True)
    call_id = fields.String(dump_only=True)
    context = fields.String(required=True)
    extension = fields.String(required=True)
    caller_id = fields.String(missing='Accent Fax')
    ivr_extension = fields.String(missing=None)
    wait_time = fields.Integer(missing=None)
    user_uuid = fields.String(dump_only=True)
    tenant_uuid = fields.String(dump_only=True)


fax_creation_request_schema = FaxCreationRequestSchema()
user_fax_creation_request_schema = UserFaxCreationRequestSchema()
fax_schema = FaxSchema()
