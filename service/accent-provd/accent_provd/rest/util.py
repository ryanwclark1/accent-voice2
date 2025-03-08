# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_provd.util import decode_bytes

PROV_MIME_TYPE = 'application/vnd.accent.provd+json'


def uri_append_path(base: bytes | str, *path: bytes | str) -> str:
    """Append path to base URI.

    >>> uri_append_path('http://localhost/', 'foo')
    'http://localhost/foo
    >>> uri_append_path('http://localhost/bar', 'foo')
    'http://localhost/bar/foo'
    >>> uri_append_path('http://localhost/bar', 'foo', 'bar')
    'http://localhost/bar/foo/bar'

    """
    if not path:
        return decode_bytes(base)
    base_decoded: str = decode_bytes(base)
    path_to_append = '/'.join(decode_bytes(p) for p in path)
    if base_decoded.endswith('/'):
        fmt = '%s%s'
    else:
        fmt = '%s/%s'
    return fmt % (base_decoded, path_to_append)
