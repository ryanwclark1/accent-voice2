# Copyright 2023 Accent Communications

import requests

from accent_calld.http_server import VERSION


# this function is not executed from the main thread
def self_check(config):
    port = config["rest_api"]["port"]
    scheme = "http"
    if config["rest_api"]["certificate"] and config["rest_api"]["private_key"]:
        scheme = "https"

    url = "{}://{}:{}/{}/status".format(scheme, "localhost", port, VERSION)
    try:
        response = requests.get(
            url, headers={'accept': 'application/json'}, verify=False
        )
        return response.status_code == 401
    except Exception:
        return False
