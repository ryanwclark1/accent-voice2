# Copyright 2023 Accent Communications

from accent_lib_rest_client import HTTPCommand


class InfosCommand(HTTPCommand):
    def __call__(self):
        return self.get()

    def get(self):
        r = self.session.get('/infos')

        return r.json()
