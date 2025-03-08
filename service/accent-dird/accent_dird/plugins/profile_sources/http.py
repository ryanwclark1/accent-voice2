# Copyright 2023 Accent Communications

from accent.tenant_flask_helpers import Tenant
from flask import request

from accent_dird.auth import required_acl
from accent_dird.http import AuthResource

from .schemas import ListSchema


class SourceResource(AuthResource):
    def __init__(self, profile_service):
        self._profile_service = profile_service

    @required_acl('dird.directories.{profile}.sources.read')
    def get(self, profile):
        args = ListSchema().load(request.args)
        tenant_uuid = Tenant.autodetect().uuid

        count, filtered, sources = self._profile_service.get_sources_from_profile_name(
            tenant_uuid=tenant_uuid, profile_name=profile, **args
        )

        return {'total': count, 'filtered': filtered, 'items': sources}
