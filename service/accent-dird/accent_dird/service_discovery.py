# Copyright 2023 Accent Communications

import requests


# this function is not executed from the main thread
def self_check(port):
    url = f'http://localhost:{port}/0.1/status'
    try:
        response = requests.get(url, headers={'accept': 'application/json'})
        return response.status_code == 401
    except Exception:
        return False
