# Copyright 2023 Accent Communications

import sys

from accent_dird import http_server
from accent_dird.plugins.base_plugins import (
    BaseServicePlugin,
    BaseSourcePlugin,
    BaseViewPlugin,
)
from accent_dird.plugins.source_result import make_result_class

# Compatibility for old plugins < 22.03
sys.modules['accent_dird.rest_api'] = sys.modules['accent_dird.http_server']

__all__ = [
    'BaseServicePlugin',
    'BaseViewPlugin',
    'BaseSourcePlugin',
    'http_server',
    'make_result_class',
]
