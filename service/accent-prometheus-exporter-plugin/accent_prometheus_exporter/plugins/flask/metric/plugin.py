# Copyright 2023 Accent Communications


import re

from prometheus_flask_exporter import PrometheusMetrics

TOKEN_URL_RE = re.compile(r"/token/([a-zA-Z0-9-]+)")
ANONYMIZED_TOKEN = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'


def path(req):
    matches = TOKEN_URL_RE.search(req.path)
    if matches:
        token = matches.group(1)
        return req.path.replace(token, ANONYMIZED_TOKEN)

    return req.path


class Plugin:
    def load(self, dependencies):
        api = dependencies['api']

        self.metrics = PrometheusMetrics(api.app, path=f'{api.prefix}/metrics', group_by=path)
