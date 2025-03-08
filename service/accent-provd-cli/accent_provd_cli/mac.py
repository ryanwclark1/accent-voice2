# Copyright 2023 Accent Communications

import re

_MAC_ADDR = re.compile(
    r'^[\da-fA-F]{1,2}([:-]?)(?:[\da-fA-F]{1,2}\1){4}[\da-fA-F]{1,2}$'
)


def _to_mac(mac_string):
    m = _MAC_ADDR.match(mac_string)
    if not m:
        raise ValueError('invalid MAC string')
    sep = m.group(1)
    if not sep:
        # no separator - length must be equal to 12 in this case
        if len(mac_string) != 12:
            raise ValueError('invalid MAC string')
        return ''.join(chr(int(mac_string[i : i + 2], 16)) for i in range(0, 12, 2))

    tokens = mac_string.split(sep)
    return ''.join(chr(int(token, 16)) for token in tokens)


def _from_mac(packed_mac, separator=':', uppercase=False):
    if len(packed_mac) != 6:
        raise ValueError('invalid packed MAC')
    if uppercase:
        fmt = '%02X'
    else:
        fmt = '%02x'
    return separator.join(fmt % ord(e) for e in packed_mac)


def norm_mac(mac_string):
    return _from_mac(_to_mac(mac_string))
