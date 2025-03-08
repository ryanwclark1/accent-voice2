# Copyright 2023 Accent Communications

import logging

from accent import rest_api_helpers

logger = logging.getLogger(__name__)


APIException = rest_api_helpers.APIException


class MasterTenantNotInitialized(APIException):
    def __init__(self):
        msg = 'accent-phoned master tenant is not initialized'
        super().__init__(503, msg, 'master-tenant-not-initialized')
