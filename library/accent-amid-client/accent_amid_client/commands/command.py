# Copyright 2023 Accent Communications

from accent_amid_client.command import AmidCommand


class CommandCommand(AmidCommand):
    resource = 'action'

    def __call__(self, command):
        body = {'command': command}
        url = f'{self.base_url}/Command'
        r = self.session.post(url, json=body)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
