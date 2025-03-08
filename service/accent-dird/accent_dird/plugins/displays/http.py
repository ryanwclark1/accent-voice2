# Copyright 2023 Accent Communications

import logging

from accent.tenant_flask_helpers import Tenant
from flask import request

from accent_dird.auth import required_acl
from accent_dird.http import AuthResource
from accent_dird.plugin_helpers.tenant import get_tenant_uuids

from .schemas import display_list_schema, display_schema, list_schema

logger = logging.getLogger(__name__)


class _BaseResource(AuthResource):
    def __init__(self, display_service):
        self._display_service = display_service


class Displays(_BaseResource):
    @required_acl('dird.displays.read')
    def get(self):
        list_params = list_schema.load(request.args)
        visible_tenants = get_tenant_uuids(recurse=list_params['recurse'])
        displays = self._display_service.list_(visible_tenants, **list_params)
        items = display_list_schema.dump(displays)
        filtered = self._display_service.count(visible_tenants, **list_params)
        total = self._display_service.count(visible_tenants)

        return {'total': total, 'filtered': filtered, 'items': items}

    @required_acl('dird.displays.create')
    def post(self):
        tenant = Tenant.autodetect()
        args = display_schema.load(request.get_json())
        body = self._display_service.create(tenant_uuid=tenant.uuid, **args)
        return display_schema.dump(body), 201


class Display(_BaseResource):
    @required_acl('dird.displays.{display_uuid}.delete')
    def delete(self, display_uuid):
        visible_tenants = get_tenant_uuids(recurse=True)
        self._display_service.delete(display_uuid, visible_tenants)
        return '', 204

    @required_acl('dird.displays.{display_uuid}.read')
    def get(self, display_uuid):
        visible_tenants = get_tenant_uuids(recurse=True)
        display = self._display_service.get(display_uuid, visible_tenants)
        return display_schema.dump(display)

    @required_acl('dird.displays.{display_uuid}.update')
    def put(self, display_uuid):
        visible_tenants = get_tenant_uuids(recurse=True)
        args = display_schema.load(request.get_json())
        self._display_service.edit(display_uuid, visible_tenants=visible_tenants, **args)
        return '', 204
