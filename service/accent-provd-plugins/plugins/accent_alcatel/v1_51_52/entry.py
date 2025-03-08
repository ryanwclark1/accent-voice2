# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from .common import BaseAlcatelMyriadPgAssociator, BaseAlcatelPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseAlcatelPlugin: type[BaseAlcatelPlugin]
        BaseAlcatelMyriadPgAssociator: type[BaseAlcatelMyriadPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODELS_VERSIONS = {
    '8028s-GE': '1.51.52',
}


class AlcatelMyriadPlugin(common['BaseAlcatelPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True
    _MODELS_VERSIONS = MODELS_VERSIONS

    pg_associator = common['BaseAlcatelMyriadPgAssociator'](MODELS_VERSIONS)
