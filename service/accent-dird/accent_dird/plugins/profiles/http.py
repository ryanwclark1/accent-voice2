# Copyright 2023 Accent Communications

import logging

from accent.tenant_flask_helpers import Tenant
from flask import request

from accent_dird.auth import required_acl
from accent_dird.http import AuthResource
from accent_dird.plugin_helpers.tenant import get_tenant_uuids

from .schemas import list_schema, profile_list_schema, profile_schema

logger = logging.getLogger(__name__)


class _BaseResource(AuthResource):
    def __init__(self, profile_service):
        self._profile_service = profile_service


class Profiles(_BaseResource):
    @required_acl('dird.profiles.read')
    def get(self):
        list_params = list_schema.load(request.args)
        visible_tenants = get_tenant_uuids(recurse=list_params['recurse'])
        profiles = self._profile_service.list_(visible_tenants, **list_params)
        items = profile_list_schema.dump(profiles)
        filtered = self._profile_service.count(visible_tenants, **list_params)
        total = self._profile_service.count(visible_tenants)

        return {'total': total, 'filtered': filtered, 'items': items}

    @required_acl('dird.profiles.create')
    def post(self):
        tenant = Tenant.autodetect()
        args = profile_schema.load(request.get_json())
        body = self._profile_service.create(tenant_uuid=tenant.uuid, **args)
        return profile_schema.dump(body), 201


class Profile(_BaseResource):
    @required_acl('dird.profiles.{profile_uuid}.delete')
    def delete(self, profile_uuid):
        visible_tenants = get_tenant_uuids(recurse=True)
        self._profile_service.delete(profile_uuid, visible_tenants)
        return '', 204

    @required_acl('dird.profiles.{profile_uuid}.read')
    def get(self, profile_uuid):
        visible_tenants = get_tenant_uuids(recurse=True)
        profile = self._profile_service.get(profile_uuid, visible_tenants)
        return profile_schema.dump(profile)

    @required_acl('dird.profiles.{profile_uuid}.update')
    def put(self, profile_uuid):
        visible_tenants = get_tenant_uuids(recurse=True)
        args = profile_schema.load(request.get_json())
        self._profile_service.edit(profile_uuid, visible_tenants=visible_tenants, **args)
        return '', 204
