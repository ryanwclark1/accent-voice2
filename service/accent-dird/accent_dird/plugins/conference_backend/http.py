# Copyright 2023 Accent Communications

from flask import request

from accent_dird import exception
from accent_dird.auth import required_acl
from accent_dird.helpers import SourceItem, SourceList
from accent_dird.http import AuthResource
from accent_dird.plugin_helpers.confd_client_registry import registry
from accent_dird.plugin_helpers.tenant import get_tenant_uuids

from .schemas import (
    contact_list_param_schema,
    contact_list_schema,
    list_schema,
    source_list_schema,
    source_schema,
)


class ConferenceList(SourceList):
    list_schema = list_schema
    source_schema = source_schema
    source_list_schema = source_list_schema

    @required_acl('dird.backends.conference.sources.read')
    def get(self):
        return super().get()

    @required_acl('dird.backends.conference.sources.create')
    def post(self):
        return super().post()


class ConferenceItem(SourceItem):
    source_schema = source_schema

    @required_acl('dird.backends.conference.sources.{source_uuid}.delete')
    def delete(self, source_uuid):
        return super().delete(source_uuid)

    @required_acl('dird.backends.conference.sources.{source_uuid}.read')
    def get(self, source_uuid):
        return super().get(source_uuid)

    @required_acl('dird.backends.conference.sources.{source_uuid}.update')
    def put(self, source_uuid):
        return super().put(source_uuid)


class ConferenceContactList(AuthResource):
    def __init__(self, source_service):
        self._source_service = source_service

    @required_acl('dird.backends.conference.sources.{source_uuid}.contacts.read')
    def get(self, source_uuid):
        visible_tenants = get_tenant_uuids(recurse=True)
        list_params = contact_list_param_schema.load(request.args)
        source_config = self._source_service.get('conference', source_uuid, visible_tenants)

        confd = registry.get(source_config)
        try:
            response = confd.conferences.list(**list_params)
        except Exception as e:
            raise exception.AccentConfdError(confd, e)

        return {
            'total': response['total'],
            'filtered': response['total'],
            'items': contact_list_schema.dump(response['items']),
        }
