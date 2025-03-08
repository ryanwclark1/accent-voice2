# Copyright 2023 Accent Communications


class DirdProfileService:
    def __init__(self, dird_client):
        self._dird = dird_client

    def list(self):
        return self._dird.profiles.list()

    def get(self, uuid):
        return self._dird.profiles.get(uuid)

    def update(self, profile_data):
        return self._dird.profiles.edit(profile_data['uuid'], profile_data)
