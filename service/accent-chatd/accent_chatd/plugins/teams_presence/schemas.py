# Copyright 2023 Accent Communications

from accent.mallow import fields
from accent.mallow.validate import OneOf
from accent.mallow_helpers import Schema


class PresenceResourceSchema(Schema):
    id = fields.String(load_only=True, required=True)
    activity = fields.String(load_only=True, missing='', allow_none=False)
    availability = fields.String(
        load_only=True,
        required=True,
        validate=OneOf(
            [
                'Available',
                'AvailableIdle',
                'Away',
                'BeRightBack',
                'Busy',
                'BusyIdle',
                'DoNotDisturb',
                'Offline',
                'PresenceUnknown',
            ]
        ),
    )


class ResourceDataSchema(Schema):
    id = fields.String(required=True)


class SubscriptionResourceSchema(Schema):
    subscription_id = fields.UUID(load_only=True, data_key='subscriptionId')
    change_type = fields.String(load_only=True, required=True, data_key='changeType')
    resource = fields.String(load_only=True, required=True)
    expiration = fields.DateTime(
        format='iso',
        load_only=True,
        required=True,
        data_key='subscriptionExpirationDateTime',
    )
    client_state = fields.String(load_only=True, data_key='clientState')
    resource_data = fields.Nested(
        ResourceDataSchema, many=False, required=True, data_key='resourceData'
    )


class TeamsSubscriptionSchema(Schema):
    value = fields.Nested(
        SubscriptionResourceSchema, many=True, required=True, data_key='value'
    )
