# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import BaseDigiumPlugin, DigiumPgAssociator  # noqa: F401

    class CommonGlobalsDict(TypedDict):
        BaseDigiumPlugin: type[BaseDigiumPlugin]
        DigiumPgAssociator: type[DigiumPgAssociator]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]


VERSION = '2.2.1.8'


class DigiumPlugin(common['BaseDigiumPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    pg_associator = common['DigiumPgAssociator'](VERSION)
