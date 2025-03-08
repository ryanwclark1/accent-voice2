# Copyright 2023 Accent Communications

import logging

from psycopg2.extras import DictCursor

from accent_agid import agid

logger = logging.getLogger(__name__)

VARIABLE_MAP = {
    'ACCENT_CALLOPTIONS': 'ACCENT_CALLOPTIONS',
    'ACCENT_CONTEXT': 'ACCENT_CONTEXT',
    'ACCENT_DSTID': 'ACCENT_DSTID',
    'ACCENT_DSTNUM': 'ACCENT_DSTNUM',
    'ACCENT_INTERFACE': 'ACCENT_INTERFACE',
    'ACCENT_GROUPNAME': 'ACCENT_GROUPNAME',
    'ACCENT_GROUPOPTIONS': 'ACCENT_GROUPOPTIONS',
    'ACCENT_QUEUENAME': 'ACCENT_QUEUENAME',
    'ACCENT_PICKEDUP': 'ACCENT_PICKEDUP',
    'ACCENT_RINGSECONDS': 'ACCENT_RINGSECONDS',
    'ACCENT_CALLORIGIN': 'ACCENT_CALLORIGIN',
    'ACCENT_MOBILEPHONENUMBER': 'ACCENT_MOBILEPHONENUMBER',
    'ACCENT_QUEUEOPTIONS': 'ACCENT_QUEUEOPTIONS',
    'ACCENT_SRCNUM': 'ACCENT_SRCNUM',
    'ACCENT_DST_EXTEN_ID': 'ACCENT_DST_EXTEN_ID',
    'ACCENT_FWD_REFERER': 'ACCENT_FWD_REFERER',
    'ACCENT_FROMGROUP': 'ACCENT_FROMGROUP',
    'ACCENT_BASE_CONTEXT': 'ACCENT_BASE_CONTEXT',
    'ACCENT_ENABLEDND': 'ACCENT_ENABLEDND',
    'ACCENT_ENABLEUNC': 'ACCENT_ENABLEUNC',
    'ACCENT_SIMULTCALLS': 'ACCENT_SIMULTCALLS',
}
ORIG_VALUE_TPL = 'ACCENT_COMPAT_{new_name}_ORIG'


def pre_subroutine_compat(
    agi: agid.FastAGI, cursor: DictCursor, args: list[str]
) -> None:
    logger.debug('Entering pre-subroutine compatibility')
    for new_name, old_name in VARIABLE_MAP.items():
        current_value = agi.get_variable(new_name)
        agi.set_variable(old_name, current_value)
        agi.set_variable(ORIG_VALUE_TPL.format(new_name=new_name), current_value)


def post_subroutine_compat(
    agi: agid.FastAGI, cursor: DictCursor, args: list[str]
) -> None:
    logger.debug('Entering post-subroutine compatibility')
    for new_name, old_name in VARIABLE_MAP.items():
        orig_value = agi.get_variable(ORIG_VALUE_TPL.format(new_name=new_name))
        new_value = agi.get_variable(new_name)
        compat_value = agi.get_variable(old_name)

        # Cleanup the mess to make sure it does not get used
        agi.set_variable(old_name, '')
        agi.set_variable(ORIG_VALUE_TPL.format(new_name=new_name), '')

        # Nothing changed, keep going
        if new_value == orig_value == compat_value:
            continue

        # New name has been used everything is fine
        if new_value != orig_value:
            continue

        # The old variable name has been used
        if compat_value != orig_value:
            msg = (
                f'The deprecated variable {old_name} has been modified by a subroutine.'
                f' Use {new_name} instead'
            )
            logger.info(msg)
            agi.verbose(msg)
            agi.set_variable(new_name, compat_value)


agid.register(pre_subroutine_compat)
agid.register(post_subroutine_compat)
