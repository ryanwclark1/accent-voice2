# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import (  # noqa: F401
        BaseGrandstreamPgAssociator,
        BaseGrandstreamPlugin,
    )

    class CommonGlobalsDict(TypedDict):
        BaseGrandstreamPlugin: type[BaseGrandstreamPlugin]
        BaseGrandstreamPgAssociator: type[BaseGrandstreamPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODELS = [
    'GXP1610',
    'GXP1615',
    'GXP1620',
    'GXP1625',
    'GXP1628',
    'GXP1630',
]
VERSION = '1.0.7.13'


class GrandstreamPlugin(common['BaseGrandstreamPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _MODELS = MODELS

    pg_associator = common['BaseGrandstreamPgAssociator'](MODELS, VERSION)
