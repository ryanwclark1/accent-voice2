# Copyright 2023 Accent Communications

from ..command import CalldCommand


class MeetingsCommand(CalldCommand):
    resource = 'meetings'

    def guest_status(self, meeting_uuid):
        headers = self._get_headers()
        url = self._client.url(
            'guests',
            'me',
            self.resource,
            meeting_uuid,
            'status',
        )
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_participants(self, meeting_uuid):
        headers = self._get_headers()
        url = self._client.url(self.resource, meeting_uuid, 'participants')
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def user_list_participants(self, meeting_uuid):
        headers = self._get_headers()
        url = self._client.url(
            'users', 'me', self.resource, meeting_uuid, 'participants'
        )
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def kick_participant(self, meeting_uuid, participant_id):
        headers = self._get_headers()
        url = self._client.url(
            self.resource, meeting_uuid, 'participants', participant_id
        )
        r = self.session.delete(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

    def user_kick_participant(self, meeting_uuid, participant_id):
        headers = self._get_headers()
        url = self._client.url(
            'users', 'me', self.resource, meeting_uuid, 'participants', participant_id
        )
        r = self.session.delete(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
