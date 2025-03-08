# Copyright 2023 Accent Communications

import requests


class WebhookdMockClient:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def url(self, *parts):
        return f'http://{self._host}:{self._port}/{"/".join(parts)}'

    def reset(self):
        requests.post(self.url('_reset'))

    def requests(self):
        return requests.get(self.url('_requests'))

    def get_config(self):
        return requests.get(self.url('1.0', 'config'))
