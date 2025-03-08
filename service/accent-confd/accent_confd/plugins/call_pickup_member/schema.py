# Copyright 2023 Accent Communications

from marshmallow import fields

from accent_confd.helpers.mallow import BaseSchema, Nested


class CallPickupInterceptorGroupSchema(BaseSchema):
    id = fields.Integer(required=True)


class CallPickupInterceptorGroupsSchema(BaseSchema):
    groups = Nested(CallPickupInterceptorGroupSchema, many=True, required=True)


class CallPickupTargetGroupSchema(BaseSchema):
    id = fields.Integer(required=True)


class CallPickupTargetGroupsSchema(BaseSchema):
    groups = Nested(CallPickupTargetGroupSchema, many=True, required=True)


class CallPickupInterceptorUserSchema(BaseSchema):
    uuid = fields.String(required=True)


class CallPickupInterceptorUsersSchema(BaseSchema):
    users = Nested(CallPickupInterceptorUserSchema, many=True, required=True)


class CallPickupTargetUserSchema(BaseSchema):
    uuid = fields.String(required=True)


class CallPickupTargetUsersSchema(BaseSchema):
    users = Nested(CallPickupTargetUserSchema, many=True, required=True)
