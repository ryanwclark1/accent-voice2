# Copyright 2023 Accent Communications

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypedDict

    from ..common.common import (  # noqa: F401
        BaseFanvilHTTPDeviceInfoExtractor,
        BaseFanvilPgAssociator,
        BaseFanvilPlugin,
    )

    class CommonGlobalsDict(TypedDict):
        BaseFanvilPlugin: type[BaseFanvilPlugin]
        BaseFanvilPgAssociator: type[BaseFanvilPgAssociator]
        BaseFanvilHTTPDeviceInfoExtractor: type[BaseFanvilHTTPDeviceInfoExtractor]


common: CommonGlobalsDict = {}  # type: ignore[typeddict-item]
execfile_('common.py', common)  # type: ignore[name-defined]

MODELS = [
    'V62',
    'V64',
    'V65',
    'V67',
]

COMMON_FILES = {
    'F0V0V6700000.cfg': (
        'V67',
        'v67_fanvil_2.6.10.1515_20240711_update_full.zip',
        'model-v.tpl',
    ),
    'fanvil_v67_hw1_1.txt': (
        'V67',
        'v67_fanvil_2.6.10.1515_20240711_update_full.zip',
        'model-v67.tpl',
    ),
    'F0V0V6200000.cfg': (
        'V62',
        'v62-fanvil-release-ff01-5944-2.12.16.17-krnvUT2023-05-05-18.17.53.z',
        'model-v6x.tpl',
    ),
    'fanvil_v62_hwv1_0.txt': (
        'V62',
        'v62-fanvil-release-ff01-5944-2.12.16.17-krnvUT2023-05-05-18.17.53.z',
        'model-v6x.tpl',
    ),
    'F0V0V6400000.cfg': (
        'V64',
        'v64-fanvil-release-ff01-5922-2.12.21.2-krnlvUT2024-08-28-09.42.06.z',
        'model-v64.tpl',
    ),
    'fanvil_v64_hwv1_0.txt': (
        'V64',
        'v64-fanvil-release-ff01-5922-2.12.21.2-krnlvUT2024-08-28-09.42.06.z',
        'model-v64.tpl',
    ),
    'F0V0V6500000.cfg': (
        'V65',
        'v65-fanvil-release-5924-2.12.21.1-krnvlT2024-08-28-09.41.46.z',
        'model-v65.tpl',
    ),
    'fanvil_v65_hwv1_0.txt': (
        'V65',
        'v65-fanvil-release-5924-2.12.21.1-krnvlT2024-08-28-09.41.46.z',
        'model-v65.tpl',
    ),
}

MODEL_FIRMWARE_MAPPING = {
    'V67': 'v67_fanvil_2.6.10.1515_20240711_update_full.zip',
    'V65': 'v65-fanvil-release-5924-2.12.21.1-krnvlT2024-08-28-09.41.46.z',
    'V64': 'v64-fanvil-release-ff01-5922-2.12.21.2-krnlvUT2024-08-28-09.42.06.z',
    'V62': 'v62-fanvil-release-ff01-5944-2.12.16.17-krnvUT2023-05-05-18.17.53.z',
}

FUNCTION_KEYS_PER_PAGE = {
    'V67': 29,
    'V65': 9,
    'V64': 7,
    'V62': 5,
}


class FanvilPlugin(common['BaseFanvilPlugin']):  # type: ignore[valid-type,misc]
    IS_PLUGIN = True

    _COMMON_FILES = COMMON_FILES
    _MODEL_FIRMWARE_MAPPING = MODEL_FIRMWARE_MAPPING
    _FUNCTION_KEYS_PER_PAGE = FUNCTION_KEYS_PER_PAGE
    _TOP_FUNCTION_KEYS: dict[str, int] = {}
    _LINE_KEYS_PER_PAGE: dict[str, int] = {}
    _LOCALE = {
        'de_DE': '16',
        'es_ES': '6',
        'fr_FR': '5',
        'fr_CA': '5',
        'it_IT': '7',
        'nl_NL': '3',
        'en_US': '0',
    }
    _TZ_INFO = {
        -12: [('UTC-12', -48)],
        -11: [('UTC-11', -44)],
        -10: [('UTC-10', -40)],
        -9: [('UTC-09', -36)],
        -8: [('UTC-08', -32)],
        -7: [('UTC-07', -28)],
        -6: [('UTC-06', -24)],
        -5: [('UTC-05', -20)],
        -4: [('UTC-04', -16)],
        -3: [('UTC-03', -12)],
        -2: [('UTC-02', -8)],
        -1: [('UTC-01', -4)],
        0: [('UCT', 0)],
        1: [('UTC+1', 4)],
        2: [('UTC+2', 8)],
        3: [('UTC+3', 12)],
        4: [('UTC+4', 16)],
        5: [('UTC+5', 20)],
        6: [('UTC+6', 24)],
        7: [('UTC+7', 28)],
        8: [('UTC+8', 32)],
        9: [('UTC+9', 36)],
        10: [('UTC+10', 40)],
        11: [('UTC+11', 44)],
        12: [('UTC+12', 48)],
    }

    pg_associator = common['BaseFanvilPgAssociator'](MODELS)
    http_dev_info_extractor = common['BaseFanvilHTTPDeviceInfoExtractor'](_COMMON_FILES)
