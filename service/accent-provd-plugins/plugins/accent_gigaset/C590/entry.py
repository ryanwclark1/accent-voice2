# Copyright 2023 Accent Communications

"""Plugin for various Gigaset using the 025 firmware.

The following Gigaset phones are supported:
- C590 IP
- C595 IP (not tested)
- C610 IP (not tested)
- C610A IP (not tested)
- N300 IP (not tested)
- N300A IP (not tested)

"""
from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common_c.common import (  # noqa: F401
        BaseGigasetPgAssociator,
        BaseGigasetPlugin,
        BaseGigasetRequestBroker,
        GigasetInteractionError,
    )

    class CommonGlobalsDict(TypedDict):
        BaseGigasetRequestBroker: type[BaseGigasetRequestBroker]
        BaseGigasetPlugin: type[BaseGigasetPlugin]
        BaseGigasetPgAssociator: type[BaseGigasetPgAssociator]
        GigasetInteractionError: type[GigasetInteractionError]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

logger = logging.getLogger('plugin.accent-gigaset')


MODELS = ['C590 IP', 'C595 IP', 'C610 IP', 'C610A IP', 'N300 IP', 'N300A IP']


class GigasetRequestBroker(common_globals['BaseGigasetRequestBroker']):  # type: ignore[valid-type,misc]  # noqa
    _VERSION_REGEX = re.compile(r'\b42(\d{3})')

    def disable_gigasetnet_line(self):
        # we need to first check if the line is enabled or not...
        with self.do_get_request('scripts/settings_telephony_voip_multi.js') as fobj:
            for line in fobj:
                if line.startswith('linesSHC[0][4]='):
                    if line[12:13] == '3':
                        logger.debug('gigaset line is enabled')
                        break
                    else:
                        logger.debug('gigaset line is disabled')
                        return
            else:
                raise GigasetInteractionError('Could not determine gigaset line status')

        # assert: gigaset line is enabled
        raw_data = 'account_id=6&action_type=1'
        with self.do_post_request(
            'settings_telephony_connections.html', raw_data
        ) as fobj:
            fobj.read()

    def set_mailboxes(self, dict_):
        # dict_ is a dictionary where keys are line number and values are
        # mailbox extensions number
        raw_data = {}
        for id_no in range(8):
            line_no = id_no + 1
            if line_no in dict_:
                raw_data[f'ad_number_{id_no}'] = dict_[line_no]
                raw_data[f'ad_active_{id_no}'] = 'on'
            else:
                raw_data[f'ad_number_{id_no}'] = ''
        with self.do_post_request(
            'settings_telephony_network_mailboxes.html', raw_data
        ) as fobj:
            fobj.read()


class GigasetPlugin(common_globals['BaseGigasetPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _BROKER_FACTORY = GigasetRequestBroker

    pg_associator = common_globals['BaseGigasetPgAssociator'](MODELS)
