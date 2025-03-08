# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BaseCiscoPgAssociator, BaseCiscoSccpPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseCiscoSccpPlugin: type[BaseCiscoSccpPlugin]
        BaseCiscoPgAssociator: type[BaseCiscoPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODELS = ['7921G']


class CiscoSccpPlugin(common['BaseCiscoSccpPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common['BaseCiscoPgAssociator'](MODELS)
