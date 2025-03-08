# Copyright 2023 Accent Communications

import requests


class ARIClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def url(self, *parts):
        return 'http://{host}:{port}/{path}'.format(
            host=self.host, port=self.port, path='/'.join(parts)
        )

    def set_sounds(self, sounds):
        url = self.url('_set_response')
        body = {'response': 'sounds', 'content': sounds}
        requests.post(url, json=body)

    def set_sound(self, sound):
        url = self.url('_set_response')
        body = {'response': 'sounds/{}'.format(sound['id']), 'content': sound}
        requests.post(url, json=body)

    def reset(self):
        url = self.url('_reset')
        requests.post(url)

    def requests(self):
        url = self.url('_requests')
        return requests.get(url).json()
