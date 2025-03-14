# Copyright 2023 Accent Communications

import requests

from accent_auth.http_server import VERSION


# this function is not executed from the main thread
def self_check(config):
    port = config['rest_api']['port']
    scheme = "http"
    if config['rest_api']['certificate'] and config['rest_api']['private_key']:
        scheme = 'https'

    host = 'localhost'
    endpoint = 'backends'
    url = f'{scheme}://{host}:{port}/{VERSION}/{endpoint}'
    headers = {'accept': 'application/json'}
    try:
        return requests.get(url, headers=headers, verify=False).status_code == 200
    except Exception:
        return False
