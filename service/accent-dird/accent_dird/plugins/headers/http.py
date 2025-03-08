# Copyright 2023 Accent Communications

import logging

from accent.tenant_flask_helpers import Tenant

from accent_dird.auth import required_acl
from accent_dird.exception import OldAPIException
from accent_dird.helpers import DisplayAwareResource
from accent_dird.http import LegacyAuthResource

logger = logging.getLogger(__name__)


class Headers(LegacyAuthResource, DisplayAwareResource):
    def __init__(self, display_service, profile_service):
        self.display_service = display_service
        self.profile_service = profile_service

    @required_acl('dird.directories.lookup.{profile}.headers.read')
    def get(self, profile):
        logger.debug('header request on profile %s', profile)
        tenant = Tenant.autodetect()
        try:
            profile_config = self.profile_service.get_by_name(tenant.uuid, profile)
            display = self.build_display(profile_config)
        except OldAPIException as e:
            return e.body, e.status_code
        response = format_headers(display)
        return response


def format_headers(display):
    return {
        'column_headers': [d.title for d in display],
        'column_types': [d.type for d in display],
    }
