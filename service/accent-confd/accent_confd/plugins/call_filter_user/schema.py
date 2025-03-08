# Copyright 2023 Accent Communications

from marshmallow import fields, post_load
from marshmallow.validate import Range

from accent_confd.helpers.mallow import BaseSchema, Nested


class CallFilterRecipientUserSchema(BaseSchema):
    uuid = fields.String(required=True)
    timeout = fields.Integer(validate=Range(min=0), allow_none=True, missing=None)

    @post_load
    def add_envelope(self, data, **kwargs):
        data['user'] = {'uuid': data.pop('uuid')}
        return data


class CallFilterRecipientUsersSchema(BaseSchema):
    users = Nested(CallFilterRecipientUserSchema, many=True, required=True)


class CallFilterSurrogateUserSchema(BaseSchema):
    uuid = fields.String(required=True)

    @post_load
    def add_envelope(self, data, **kwargs):
        data['user'] = {'uuid': data.pop('uuid')}
        return data


class CallFilterSurrogateUsersSchema(BaseSchema):
    users = Nested(CallFilterSurrogateUserSchema, many=True, required=True)
