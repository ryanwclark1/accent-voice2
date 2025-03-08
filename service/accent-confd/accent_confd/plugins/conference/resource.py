# Copyright 2023 Accent Communications

from accent_dao.alchemy.conference import Conference
from flask import url_for

from accent_confd.auth import required_acl
from accent_confd.helpers.restful import ItemResource, ListResource

from .schema import ConferenceSchema


class ConferenceList(ListResource):
    model = Conference
    schema = ConferenceSchema

    def build_headers(self, conference):
        return {'Location': url_for('conferences', id=conference.id, _external=True)}

    @required_acl('confd.conferences.create')
    def post(self):
        return super().post()

    @required_acl('confd.conferences.read')
    def get(self):
        return super().get()


class ConferenceItem(ItemResource):
    schema = ConferenceSchema
    has_tenant_uuid = True

    @required_acl('confd.conferences.{id}.read')
    def get(self, id):
        return super().get(id)

    @required_acl('confd.conferences.{id}.update')
    def put(self, id):
        return super().put(id)

    @required_acl('confd.conferences.{id}.delete')
    def delete(self, id):
        return super().delete(id)
