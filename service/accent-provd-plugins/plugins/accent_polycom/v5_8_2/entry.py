# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BasePolycomPgAssociator, BasePolycomPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BasePolycomPlugin: type[BasePolycomPlugin]
        BasePolycomPgAssociator: type[BasePolycomPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

MODELS = [
    'VVX101',
    'VVX150',
    'VVX201',
    'VVX250',
    'VVX300',
    'VVX301',
    'VVX310',
    'VVX311',
    'VVX350',
    'VVX400',
    'VVX401',
    'VVX450',
    'VVX410',
    'VVX411',
    'VVX500',
    'VVX501',
    'VVX600',
    'VVX601',
    'VVX1500',
]


class PolycomPlugin(common_globals['BasePolycomPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common_globals['BasePolycomPgAssociator'](MODELS)
