# Copyright 2023 Accent Communications

import requests


def self_check(port):
    url = f'http://localhost:{port}/0.2/config'
    try:
        return requests.get(url, headers={'accept': 'application/json'}, timeout=1).status_code == 401
    except Exception:
        return False
