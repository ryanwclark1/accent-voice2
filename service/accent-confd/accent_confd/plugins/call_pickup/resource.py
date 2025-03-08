# Copyright 2023 Accent Communications

from accent_dao.alchemy.pickup import Pickup as CallPickup
from flask import url_for

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ItemResource, ListResource

from .schema import CallPickupSchema


class CallPickupList(ListResource):
    model = CallPickup
    schema = CallPickupSchema

    def build_headers(self, call_pickup):
        return {'Location': url_for('callpickups', id=call_pickup.id, _external=True)}

    @required_acl('confd.callpickups.create')
    def post(self):
        return super().post()

    @required_acl('confd.callpickups.read')
    def get(self):
        return super().get()


class CallPickupItem(ItemResource):
    schema = CallPickupSchema
    has_tenant_uuid = True

    @required_acl('confd.callpickups.{id}.read')
    def get(self, id):
        return super().get(id)

    @required_acl('confd.callpickups.{id}.update')
    def put(self, id):
        return super().put(id)

    @required_acl('confd.callpickups.{id}.delete')
    def delete(self, id):
        return super().delete(id)
