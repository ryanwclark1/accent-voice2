# Copyright 2023 Accent Communications

from __future__ import annotations

from psycopg2.extras import DictCursor

from accent_agid import agid, objects


def incoming_did_set_features(
    agi: agid.FastAGI, cursor: DictCursor, args: list[str]
) -> None:
    incall_id = agi.get_variable('ACCENT_INCALL_ID')

    did = objects.DID(agi, cursor, incall_id)

    if did.preprocess_subroutine:
        preprocess_subroutine = did.preprocess_subroutine
    else:
        preprocess_subroutine = ""

    agi.set_variable('ACCENT_DIDPREPROCESS_SUBROUTINE', preprocess_subroutine)
    agi.set_variable('ACCENT_EXTENPATTERN', did.exten)
    agi.set_variable('ACCENT_PATH', 'incall')
    agi.set_variable('ACCENT_PATH_ID', did.id)
    agi.set_variable('ACCENT_REAL_CONTEXT', did.context)
    agi.set_variable('ACCENT_REAL_NUMBER', did.exten)
    agi.set_variable('ACCENT_GREETING_SOUND', did.greeting_sound or '')

    did.set_dial_actions()
    did.rewrite_cid()


agid.register(incoming_did_set_features)
