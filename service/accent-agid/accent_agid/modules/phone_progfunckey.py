# Copyright 2023 Accent Communications

from __future__ import annotations

from accent.accent_helpers import split_extension
from psycopg2.extras import DictCursor

from accent_agid import agid, objects


def phone_progfunckey(agi: agid.FastAGI, cursor: DictCursor, args: list[str]) -> None:
    userid = agi.get_variable('ACCENT_USERID')
    xlen = len(args)

    if xlen != 1:
        agi.dp_break(f"Invalid number of arguments (args: {args!r})")

    try:
        fklist = split_extension(args[0])
    except ValueError as e:
        agi.dp_break(str(e))

    if userid != fklist[0]:
        agi.dp_break(f"Wrong userid. (userid: {fklist[0]!r}, excepted: {userid!r})")

    feature = ""

    try:
        extenfeatures = objects.ExtenFeatures(agi, cursor)
        feature = extenfeatures.get_name_by_exten(fklist[1])
    except LookupError as e:
        feature = ""
        agi.verbose(str(e))

    agi.set_variable('ACCENT_PHONE_PROGFUNCKEY', ''.join(fklist[1:]))
    agi.set_variable('ACCENT_PHONE_PROGFUNCKEY_FEATURE', feature)


agid.register(phone_progfunckey)
