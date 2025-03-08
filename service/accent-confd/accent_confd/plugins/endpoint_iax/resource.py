# Copyright 2023 Accent Communications

from accent_dao.alchemy.useriax import UserIAX as IAXEndpoint
from flask import url_for

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ItemResource, ListResource

from .schema import IAXSchema


class IAXList(ListResource):
    model = IAXEndpoint
    schema = IAXSchema

    def build_headers(self, iax):
        return {'Location': url_for('endpoint_iax', id=iax.id, _external=True)}

    @required_acl('confd.endpoints.iax.read')
    def get(self):
        return super().get()

    @required_acl('confd.endpoints.iax.create')
    def post(self):
        return super().post()


class IAXItem(ItemResource):
    schema = IAXSchema
    has_tenant_uuid = True

    @required_acl('confd.endpoints.iax.{id}.read')
    def get(self, id):
        return super().get(id)

    @required_acl('confd.endpoints.iax.{id}.update')
    def put(self, id):
        return super().put(id)

    @required_acl('confd.endpoints.iax.{id}.delete')
    def delete(self, id):
        return super().delete(id)
