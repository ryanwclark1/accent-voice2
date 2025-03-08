# Copyright 2023 Accent Communications

"""Plugin for Alcatel phones using the SIP 2.01.10 firmware.

The following Alcatel "extended edition" phones are supported:
- 4008
- 4018

"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from .common import BaseAlcatelPgAssociator, BaseAlcatelPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseAlcatelPlugin: type[BaseAlcatelPlugin]
        BaseAlcatelPgAssociator: type[BaseAlcatelPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

logger = logging.getLogger('plugin.accent-alcatel')

MODELS = ['4008', '4018']
VERSION = '2.01.10'


class AlcatelPlugin(common_globals['BaseAlcatelPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BaseAlcatelPgAssociator'](MODELS, VERSION)
