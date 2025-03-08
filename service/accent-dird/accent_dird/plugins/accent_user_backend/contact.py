# Copyright 2023 Accent Communications

from accent_dird import exception


class ContactLister:
    def __init__(self, client):
        self._client = client

    def list(self, *args, **kwargs):
        try:
            return self._client.users.list(*args, view='directory', **kwargs)
        except Exception as e:
            raise exception.AccentConfdError(self._client, e)
