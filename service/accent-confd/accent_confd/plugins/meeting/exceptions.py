# Copyright 2023 Accent Communications

from accent.rest_api_helpers import APIException


class MeetingGuestSIPTemplateNotFound(APIException):
    def __init__(self, tenant_uuid):
        self.msg = (
            f'Could not find SIP template for meeting guests in tenant {tenant_uuid}'
        )
        details = {
            'tenant_uuid': tenant_uuid,
        }
        super().__init__(
            503,
            self.msg,
            'meeting-guest-sip-template-not-found',
            details=details,
            resource='meeting',
        )

    def __str__(self):
        return self.msg
