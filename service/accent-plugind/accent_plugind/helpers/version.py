# Copyright 2023 Accent Communications

from distutils.version import LooseVersion


def less_than(left, right):
    if not left:
        return True
    if not right:
        return False

    left = _make_comparable_version(left)
    right = _make_comparable_version(right)

    return left < right


def _make_comparable_version(version):
    try:
        value_tmp = LooseVersion(version)
        value_tmp.version  # raise AttributeError if value is None
        version = value_tmp
    except (TypeError, AttributeError):
        # Integer raise TypeError
        # Not a valid version number fallback to alphabetic ordering
        version = str(version)

    return version
