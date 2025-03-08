# Copyright 2023 Accent Communications

import argparse
import logging
from datetime import datetime, timedelta, timezone

from accent import accent_logging
from accent.chain_map import ChainMap
from accent.config_helper import read_config_file_hierarchy
from accent_auth_client import Client as AuthClient
from accent_dao import init_db_from_config
from accent_dao.helpers.db_utils import session_scope
from accent_dao.resources.infos import dao as info_dao
from accent_dao.resources.meeting import dao as meeting_dao
from accent_dao.resources.meeting_authorization import dao as meeting_authorization_dao

from accent_confd._bus import BusPublisher
from accent_confd._sysconfd import SysconfdPublisher
from accent_confd.config import DEFAULT_CONFIG, _load_key_file
from accent_confd.helpers.resource import CRUDService
from accent_confd.plugins.extension_feature.service import (
    build_service as build_extension_features_service,
)
from accent_confd.plugins.ingress_http.service import (
    build_service as build_ingress_http_service,
)
from accent_confd.plugins.meeting.notifier import Notifier as MeetingNotifier
from accent_confd.plugins.meeting.validator import (
    build_validator as build_meeting_validator,
)
from accent_confd.plugins.meeting_authorization.notifier import (
    Notifier as MeetingAuthorizationNotifier,
)
from accent_confd.plugins.meeting_authorization.service import (
    build_service as build_authorization_service,
)

logger = logging.getLogger('accent-confd-purge-meetings')


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help="Log debug messages",
    )
    parser.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='Only print warnings and errors',
    )
    parser.add_argument(
        '--authorizations-only',
        action='store_true',
        help='Only remove old meeting authorizations, not meeting themselves.',
    )
    parsed_args = parser.parse_args()
    result = {'log_level': logging.INFO}
    if parsed_args.quiet:
        result['log_level'] = logging.WARNING
    elif parsed_args.debug:
        result['log_level'] = logging.DEBUG
    result['authorizations_only'] = parsed_args.authorizations_only
    return result


def load_config():
    file_config = read_config_file_hierarchy(ChainMap(DEFAULT_CONFIG))
    service_key = _load_key_file(ChainMap(file_config, DEFAULT_CONFIG))
    return ChainMap(service_key, file_config, DEFAULT_CONFIG)


def remove_meetings_older_than(date, meeting_service):
    logger.info('Removing meetings older than %s...', date)

    with session_scope() as session:
        meetings = meeting_dao.find_all_by(created_before=date, persistent=False)
        logger.info('Found %s meeting.', len(meetings))
        for meeting in meetings:
            logger.debug('Removing meeting %s: %s', meeting.uuid, meeting.name)
            meeting_service.delete(meeting)
        session.flush()


def remove_meeting_authorizations_older_than(date, meeting_authorization_service):
    logger.info('Removing meeting authorizations older than %s...', date)

    with session_scope() as session:
        meeting_authorizations = meeting_authorization_dao.find_all_by(
            meeting_uuid=None,
            created_before=date,
        )
        logger.info('Found %s meeting authorizations.', len(meeting_authorizations))
        for meeting_authorization in meeting_authorizations:
            logger.debug(
                'Removing authorization for meeting %s: uuid "%s", guest_name "%s"',
                meeting_authorization.meeting_uuid,
                meeting_authorization.uuid,
                meeting_authorization.guest_name,
            )
            meeting_authorization_service.delete(meeting_authorization)
        session.flush()


def get_master_tenant_uuid(auth_config):
    client = AuthClient(**auth_config)
    token_data = client.token.new(expiration=1)
    return token_data['metadata']['tenant_uuid']


def main():
    cli_args = parse_cli_args()
    config = load_config()
    accent_logging.setup_logging('/dev/null', log_level=cli_args['log_level'])
    accent_logging.silence_loggers(['stevedore.extension'], logging.WARNING)

    tenant_uuid = get_master_tenant_uuid(config['auth'])
    init_db_from_config(config)

    accent_uuid = info_dao.get().uuid
    if 'uuid' not in config:
        config['uuid'] = accent_uuid

    bus = BusPublisher.from_config(config['uuid'], config['bus'])
    sysconfd = SysconfdPublisher.from_config(config)

    if not cli_args['authorizations_only']:
        ingress_http_service = build_ingress_http_service()
        extension_features_service = build_extension_features_service()
        meeting_service = CRUDService(
            meeting_dao,
            build_meeting_validator(),
            MeetingNotifier(
                bus,
                sysconfd,
                ingress_http_service,
                extension_features_service,
                tenant_uuid,
            ),
        )

        meeting_date_limit = datetime.now(timezone.utc) - timedelta(hours=24)
        remove_meetings_older_than(meeting_date_limit, meeting_service)

    authorization_notifier = MeetingAuthorizationNotifier(bus)
    meeting_authorization_service = build_authorization_service(authorization_notifier)

    meeting_authorization_date_limit = datetime.now(timezone.utc) - timedelta(hours=24)
    remove_meeting_authorizations_older_than(
        meeting_authorization_date_limit, meeting_authorization_service
    )

    sysconfd.flush()
    bus.flush()
