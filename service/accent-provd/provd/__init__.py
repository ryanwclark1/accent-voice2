# Copyright 2023 Accent Communications

import sys
import warnings

import accent_provd

warnings.simplefilter('module', category=DeprecationWarning)
warnings.warn(
    f'{__name__} is deprecated and will be removed in the future, '
    'Please use `accent_provd` instead.',
    DeprecationWarning,
    stacklevel=2,
)

# Note: Alias provd to accent_provd to keep plugins compatibility
sys.modules['provd'] = accent_provd
