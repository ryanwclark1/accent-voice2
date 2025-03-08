# Copyright 2023 Accent Communications

import requests

from accent_confd.config import API_VERSION


# this function is not executed from the main thread
def self_check(config):
    port = config["rest_api"]["port"]
    scheme = "http"
    if config["rest_api"]["certificate"] and config["rest_api"]["private_key"]:
        scheme = "https"
    url = "{}://{}:{}/{}/infos".format(scheme, "localhost", port, API_VERSION)
    try:
        return requests.get(
            url, headers={'accept': 'application/json'}, verify=False
        ).status_code in (200, 401)
    except Exception:
        return False
