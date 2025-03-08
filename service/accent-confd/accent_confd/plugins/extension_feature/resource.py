# Copyright 2023 Accent Communications

from accent_confd.auth import required_acl, required_master_tenant
from accent_confd.helpers.restful import ItemResource, ListResource

from .schema import ExtensionFeatureSchema


class ExtensionFeatureList(ListResource):
    schema = ExtensionFeatureSchema

    @required_master_tenant()
    @required_acl('confd.extensions.features.read')
    def get(self):
        return super().get()

    def post(self):
        return '', 405


class ExtensionFeatureItem(ItemResource):
    schema = ExtensionFeatureSchema

    @required_master_tenant()
    @required_acl('confd.extensions.features.{uuid}.read')
    def get(self, uuid):
        return super().get(uuid)

    @required_master_tenant()
    @required_acl('confd.extensions.features.{uuid}.update')
    def put(self, uuid):
        return super().put(uuid)

    def delete(self, uuid):
        return '', 405
