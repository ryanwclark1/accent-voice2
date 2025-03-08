# Copyright 2023 Accent Communications

from urllib import parse


def extract_connection_params(headers):
    result = {}

    parsed = parse.urlsplit(f'//{headers["Host"]}')
    if parsed.hostname:
        result['hostname'] = parsed.hostname
    if parsed.port:
        result['port'] = parsed.port

    prefix = headers.get('X-Script-Name')
    if prefix:
        result['prefix'] = prefix

    return result
