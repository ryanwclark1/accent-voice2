# Copyright 2023 Accent Communications

from __future__ import annotations

import logging
from typing import Any, Literal

logger = logging.getLogger(__name__)

SERVICE_URL_FORMAT = (
    '{scheme}://{hostname}:{port}/0.1/{vendor}/'
    'users/{user_uuid}/services/{service}/{enabled}'
)


def add_accent_phoned_user_service_url(
    raw_config: dict[str, Any],
    vendor: str,
    service_name: str,
) -> None:
    # NOTE: phoned is actually exposed as the phonebook.
    if not (hostname := raw_config.get('X_accent_phonebook_ip')):
        logger.warning(
            'Not adding XX_accent_phoned_user_service_%s_url: no hostname', service_name
        )
        return

    if not (user_uuid := raw_config.get('X_accent_user_uuid')):
        logger.warning(
            'Not adding XX_accent_phoned_user_service_%s_url: no user uuid', service_name
        )
        return

    scheme = raw_config.get('X_accent_phonebook_scheme', 'http')
    port = raw_config.get('X_accent_phonebook_port', 9498)

    formatted_enabled_url = SERVICE_URL_FORMAT.format(
        scheme=scheme,
        hostname=hostname,
        port=port,
        vendor=vendor,
        service=service_name,
        user_uuid=user_uuid,
        enabled=_enable_string(True),
    )

    formatted_disabled_url = SERVICE_URL_FORMAT.format(
        scheme=scheme,
        hostname=hostname,
        port=port,
        vendor=vendor,
        service=service_name,
        user_uuid=user_uuid,
        enabled=_enable_string(False),
    )
    raw_config[
        f'XX_accent_phoned_user_service_{service_name}_enabled_url'
    ] = formatted_enabled_url

    raw_config[
        f'XX_accent_phoned_user_service_{service_name}_disabled_url'
    ] = formatted_disabled_url


def _enable_string(enabled: bool) -> Literal['enable', 'disable']:
    if enabled:
        return 'enable'
    return 'disable'
