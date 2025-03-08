# Copyright 2023 Accent Communications

from .helpers.base import BaseCommand


class AgentStatisticsCommand(BaseCommand):
    def get_by_id(self, agent_id, **params):
        if 'from_' in params:
            params['from'] = params.pop('from_')

        headers = self._get_headers()
        url = self._client.url('agents', agent_id, 'statistics')
        r = self.session.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()

    def list(self, **params):
        if 'from_' in params:
            params['from'] = params.pop('from_')

        headers = self._get_headers()
        url = self._client.url('agents', 'statistics')
        r = self.session.get(url, params=params, headers=headers)
        self.raise_from_response(r)
        return r.json()
