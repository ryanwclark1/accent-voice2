# Copyright 2023 Accent Communications

from accent_lib_rest_client import HTTPCommand


class StatusCommand(HTTPCommand):
    def __call__(self):
        return self.get()

    def get(self):
        r = self.session.get('/status')

        return r.json()
