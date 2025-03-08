# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_dao.resources.conference import dao as conference_dao
from psycopg2.extras import DictCursor

from accent_agid import agid


def incoming_conference_set_features(
    agi: agid.FastAGI, cursor: DictCursor, args: list[str]
) -> None:
    conference_id = int(agi.get_variable('ACCENT_DSTID'))

    try:
        conference = conference_dao.get(conference_id)
    except ValueError as e:
        agi.dp_break(str(e))

    menu = 'accent-default-user-menu'
    user_profile = f'accent-user-profile-{conference.id}'
    if conference.pin:
        for _ in range(4):
            agi.answer()
            pin = agi.get_data('conf-getpin', 10000, 80)
            if pin == conference.pin:
                break
            elif pin == conference.admin_pin:
                menu = 'accent-default-admin-menu'
                user_profile = f'accent-admin-profile-{conference.id}'
                break
            else:
                agi.stream_file('conf-invalidpin')
        else:
            agi.dp_break(
                'Unable to join the conference room, wrong pin'
                f'(conference_id: {conference.id}, name: {conference.name})'
            )

    agi.set_variable('ACCENT_CONFBRIDGE_ID', conference.id)
    agi.set_variable('ACCENT_CONFBRIDGE_TENANT_UUID', conference.tenant_uuid)
    agi.set_variable(
        'ACCENT_CONFBRIDGE_BRIDGE_PROFILE', f'accent-bridge-profile-{conference.id}'
    )
    agi.set_variable('ACCENT_CONFBRIDGE_USER_PROFILE', user_profile)
    agi.set_variable('ACCENT_CONFBRIDGE_MENU', menu)
    agi.set_variable(
        'ACCENT_CONFBRIDGE_PREPROCESS_SUBROUTINE', conference.preprocess_subroutine or ''
    )
    agi.appexec('CELGenUserEvent', f'ACCENT_CONFERENCE, NAME: {conference.name or ""}')


agid.register(incoming_conference_set_features)
