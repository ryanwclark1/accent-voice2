# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BasePattonPgAssociator, BasePattonPlugin  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BasePattonPlugin: type[BasePattonPlugin]
        BasePattonPgAssociator: type[BasePattonPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODELS = [
    'SN4112',
    'SN4112S',
    'SN4114',
    'SN4116',
    'SN4118',
    'SN4316',
    'SN4324',
    'SN4332',
]
VERSION = '6.11'


class PattonPlugin(common['BasePattonPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common['BasePattonPgAssociator'](MODELS, VERSION)
