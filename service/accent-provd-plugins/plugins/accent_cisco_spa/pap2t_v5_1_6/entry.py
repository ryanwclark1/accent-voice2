# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BaseCiscoPgAssociator, BaseCiscoPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseCiscoPlugin: type[BaseCiscoPlugin]
        BaseCiscoPgAssociator: type[BaseCiscoPgAssociator]


common_globals: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common_globals)  # type: ignore[name-defined]

MODEL_VERSION = {'PAP2T': '5.1.6'}


class CiscoPlugin(common_globals['BaseCiscoPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
    _COMMON_FILENAMES = ['init.cfg']

    pg_associator = common_globals['BaseCiscoPgAssociator'](MODEL_VERSION)
