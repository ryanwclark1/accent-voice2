# Copyright 2023 Accent Communications

import requests


class AmidClient:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def url(self, *parts):
        return f'http://{self._host}:{self._port}/{"/".join(parts)}'

    def set_queuepause(self):
        url = self.url('_set_response_action')
        body = {'response': 'QueuePause', 'content': []}
        requests.post(url, json=body)
