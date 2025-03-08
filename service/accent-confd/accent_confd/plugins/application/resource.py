# Copyright 2023 Accent Communications

from accent_dao.alchemy.application import Application
from flask import url_for

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ItemResource, ListResource

from .schema import ApplicationSchema


class ApplicationList(ListResource):
    model = Application
    schema = ApplicationSchema

    def build_headers(self, application):
        return {
            'Location': url_for(
                'applications', application_uuid=application.uuid, _external=True
            )
        }

    @required_acl('confd.applications.create')
    def post(self):
        return super().post()

    @required_acl('confd.applications.read')
    def get(self):
        return super().get()


class ApplicationItem(ItemResource):
    schema = ApplicationSchema
    has_tenant_uuid = True

    @required_acl('confd.applications.{application_uuid}.read')
    def get(self, application_uuid):
        return super().get(application_uuid)

    @required_acl('confd.applications.{application_uuid}.update')
    def put(self, application_uuid):
        return super().put(application_uuid)

    @required_acl('confd.applications.{application_uuid}.delete')
    def delete(self, application_uuid):
        return super().delete(application_uuid)
