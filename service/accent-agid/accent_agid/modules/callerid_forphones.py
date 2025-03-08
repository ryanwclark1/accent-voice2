# Copyright 2023 Accent Communications

from __future__ import annotations

import logging

import phonenumbers
from accent_dao.resources.directory_profile import dao as directory_profile_dao
from accent_dird_client.client import DirdClient
from psycopg2.extras import DictCursor

from accent_agid import agid

logger = logging.getLogger(__name__)

FAKE_ACCENT_USER_UUID = '00000000-0000-0000-0000-000000000000'


def callerid_forphones(agi: agid.FastAGI, cursor: DictCursor, args: list[str]) -> None:
    dird_client: DirdClient = agi.config['dird']['client']
    try:
        cid_name = agi.env['agi_calleridname']
        cid_number = agi.env['agi_callerid']

        logger.debug(
            'Resolving caller ID: incoming caller ID=%s %s', cid_name, cid_number
        )
        if not _should_reverse_lookup(cid_name, cid_number):
            return

        incall_id = int(agi.get_variable('ACCENT_INCALL_ID'))
        callee_info = directory_profile_dao.find_by_incall_id(incall_id)
        if callee_info is None:
            user_uuid = FAKE_ACCENT_USER_UUID
        else:
            user_uuid = callee_info.accent_user_uuid

        tenant_uuid = agi.get_variable('ACCENT_TENANT_UUID')
        # It is not possible to associate a profile to a reverse configuration in the web
        lookup_result = dird_client.directories.reverse(
            profile='default',
            user_uuid=user_uuid,
            exten=cid_number,
            tenant_uuid=tenant_uuid,
        )
        if lookup_result['display'] is not None:
            logger.debug(
                'Found caller ID from reverse lookup: "%s"<%s>',
                lookup_result['display'],
                cid_number,
            )
            _set_new_caller_id(agi, lookup_result['display'], cid_number)
            _set_reverse_lookup_variable(agi, lookup_result['fields'])
    except Exception as e:
        msg = f'Reverse lookup failed: {e}'
        logger.info(msg)
        agi.verbose(msg)


def is_phone_number(cid_name: str) -> bool:
    try:
        phonenumbers.parse(cid_name, None)
    except phonenumbers.phonenumberutil.NumberParseException as ex:
        # if error is due to country code not being recognized,
        # we can assume this is a national or local number format
        return (
            ex.error_type
            == phonenumbers.phonenumberutil.NumberParseException.INVALID_COUNTRY_CODE
        )
    else:
        return True


def _should_reverse_lookup(cid_name: str, cid_number: str) -> bool:
    return cid_name == 'unknown' or is_phone_number(cid_name)


def _set_new_caller_id(agi: agid.FastAGI, display_name: str, cid_number: str) -> None:
    new_caller_id = f'"{display_name}" <{cid_number}>'
    agi.set_callerid(new_caller_id)


def _set_reverse_lookup_variable(agi: agid.FastAGI, fields: dict[str, str]) -> None:
    agi.set_variable("ACCENT_REVERSE_LOOKUP", _create_reverse_lookup_variable(fields))


def _create_reverse_lookup_variable(fields: dict[str, str]) -> str:
    variable_content = [f'db-{key}: {value}' for key, value in fields.items()]
    return ','.join(variable_content)


agid.register(callerid_forphones)
