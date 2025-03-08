# Copyright 2023 Accent Communications

import logging

from accent.auth_verifier import Unauthorized, required_acl, required_tenant
from accent.flask.headers import extract_token_id_from_query_or_header
from accent.tenant_flask_helpers import user
from requests import HTTPError
from werkzeug.local import LocalProxy as Proxy

from accent_calld.exceptions import (
    MasterTenantNotInitialized,
    TokenWithUserUUIDRequiredError,
)
from accent_calld.http_server import app

logger = logging.getLogger(__name__)

__all__ = [
    'Unauthorized',
    'extract_token_id_from_query_or_header',
    'required_acl',
]


def get_token_user_uuid_from_request():
    try:
        user_uuid = user.uuid
    except HTTPError as e:
        logger.warning('HTTP error from accent-auth while getting token: %s', e)
        raise TokenWithUserUUIDRequiredError()

    if not user_uuid:
        raise TokenWithUserUUIDRequiredError()
    return user_uuid


def required_master_tenant():
    return required_tenant(master_tenant_uuid)


def init_master_tenant(token):
    tenant_uuid = token['metadata']['tenant_uuid']
    app.config['auth']['master_tenant_uuid'] = tenant_uuid
    logger.debug('Initiated master tenant UUID: %s', tenant_uuid)


def get_master_tenant_uuid():
    if not app:
        raise Exception('Flask application not configured')

    tenant_uuid = app.config['auth'].get('master_tenant_uuid')
    if not tenant_uuid:
        raise MasterTenantNotInitialized()
    return tenant_uuid


master_tenant_uuid = Proxy(get_master_tenant_uuid)
