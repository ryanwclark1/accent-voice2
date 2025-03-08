# Copyright 2023 Accent Communications

from accent.tenant_flask_helpers import Tenant
from marshmallow import fields

from accent_confd.auth import required_acl
from accent_confd.helpers.mallow import BaseSchema
from accent_confd.helpers.restful import ConfdResource


class SubscriptionCountSchema(BaseSchema):
    id = fields.Integer(attribute='subscription_type')
    count = fields.Integer()


class UserSubscription(ConfdResource):
    schema = SubscriptionCountSchema

    def __init__(self, service):
        super().__init__()
        self.service = service

    @required_acl('confd.users.subscriptions.read')
    def get(self):
        tenant_uuid = Tenant.autodetect().uuid
        result = self.service.list(tenant_uuid)
        total = len(result)
        items = self.schema().dump(result, many=True)
        return {'total': total, 'items': items}
