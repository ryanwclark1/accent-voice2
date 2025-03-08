# Copyright 2023 Accent Communications

import requests


class AmidClient:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def url(self, *parts):
        return f'http://{self._host}:{self._port}/{"/".join(parts)}'

    def set_devicestatelist(self, *events):
        url = self.url('_set_response_action')
        body = {'response': 'DeviceStateList', 'content': events}
        requests.post(url, json=body)

    def set_coreshowchannels(self, *events):
        url = self.url('_set_response_action')
        body = {'response': 'CoreShowChannels', 'content': events}
        requests.post(url, json=body)
