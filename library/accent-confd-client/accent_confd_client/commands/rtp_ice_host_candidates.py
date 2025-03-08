# Copyright 2023 Accent Communications

from accent_lib_rest_client import RESTCommand


class RTPIceHostCandidatesCommand(RESTCommand):
    resource = 'asterisk/rtp/ice_host_candidates'

    def get(self):
        response = self.session.get(self.resource)
        return response.json()

    def update(self, body):
        self.session.put(self.resource, body)
