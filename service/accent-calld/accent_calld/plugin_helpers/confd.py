# Copyright 2023 Accent Communications

from requests import HTTPError, RequestException

from .exceptions import (
    AccentConfdUnreachable,
    InvalidUserLine,
    InvalidUserUUID,
    NoSuchConferenceID,
    NoSuchMeeting,
    NoSuchUserVoicemail,
    NoSuchVoicemail,
    UserMissingMainLine,
)


def not_found(error):
    return error.response is not None and error.response.status_code == 404


class Meeting:
    def __init__(self, tenant_uuid=None, meeting_uuid=None, confd_client=None):
        self.tenant_uuid = tenant_uuid
        self.meeting_uuid = meeting_uuid
        self._confd = confd_client

    def asterisk_name(self):
        return 'accent-meeting-{meeting_uuid}-confbridge'.format(
            meeting_uuid=self.meeting_uuid
        )

    def exists(self):
        try:
            self._confd.meetings.get(self.meeting_uuid)
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                return False
            raise
        except RequestException as e:
            raise AccentConfdUnreachable(self._confd, e)
        else:
            return True

    def is_owned_by(self, user_uuid):
        try:
            meeting = self._confd.meetings.get(self.meeting_uuid)
        except RequestException as e:
            raise AccentConfdUnreachable(self._confd, e)

        return user_uuid in meeting['owner_uuids']

    @classmethod
    def from_uuid(cls, meeting_uuid, confd_client):
        try:
            meeting = confd_client.meetings.get(meeting_uuid)
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                raise NoSuchMeeting(meeting_uuid)
            raise
        return cls(meeting['tenant_uuid'], meeting['uuid'], confd_client)


class User:
    # TODO set tenant_uuid mandatory when transfers plugin will be multi-tenant
    def __init__(self, user_uuid, confd_client, tenant_uuid=None):
        self.uuid = user_uuid
        self._tenant_uuid = tenant_uuid
        self._confd = confd_client

    @property
    def tenant_uuid(self):
        if not self._tenant_uuid:
            self._tenant_uuid = self._get_tenant_uuid()

        return self._tenant_uuid

    def assert_exists(self):
        try:
            self._confd.users.get(self.uuid, tenant_uuid=self._tenant_uuid)
        except HTTPError as e:
            if not_found(e):
                raise InvalidUserUUID(self.uuid)
            raise
        except RequestException as e:
            raise AccentConfdUnreachable(self._confd, e)

    def main_line(self):
        try:
            lines = self._confd.users.get(self.uuid, tenant_uuid=self.tenant_uuid)[
                'lines'
            ]
        except HTTPError as e:
            if not_found(e):
                raise InvalidUserUUID(self.uuid)
            raise
        except RequestException as e:
            raise AccentConfdUnreachable(self._confd, e)

        try:
            main_line_id = lines[0]['id']
        except IndexError:
            raise UserMissingMainLine(self.uuid)
        return Line(main_line_id, self._confd, tenant_uuid=self.tenant_uuid)

    def line(self, line_id):
        try:
            lines = self._confd.users.get(self.uuid, tenant_uuid=self.tenant_uuid)[
                'lines'
            ]
        except HTTPError as e:
            if not_found(e):
                raise InvalidUserUUID(self.uuid)
            raise
        except RequestException as e:
            raise AccentConfdUnreachable(self._confd, e)

        valid_line_ids = [line['id'] for line in lines]
        if line_id not in valid_line_ids:
            raise InvalidUserLine(self.uuid, line_id)

        return Line(line_id, self._confd, tenant_uuid=self.tenant_uuid)

    def mobile_phone_number(self):
        try:
            return self._confd.users.get(self.uuid, tenant_uuid=self.tenant_uuid)[
                'mobile_phone_number'
            ]
        except HTTPError as e:
            if not_found(e):
                raise InvalidUserUUID(self.uuid)
            raise
        except RequestException as e:
            raise AccentConfdUnreachable(self._confd, e)

    def _get_tenant_uuid(self):
        try:
            return self._confd.users.get(self.uuid)['tenant_uuid']
        except HTTPError as e:
            if not_found(e):
                raise InvalidUserUUID(self.uuid)
            raise
        except RequestException as e:
            raise AccentConfdUnreachable(self._confd, e)


class Line:
    # TODO set tenant_uuid mandatory when transfers plugin will be multi-tenant
    def __init__(self, line_id, confd_client, tenant_uuid=None):
        self.id = line_id
        self._confd = confd_client
        self.tenant_uuid = tenant_uuid

    def _get(self):
        try:
            return self._confd.lines.get(self.id, tenant_uuid=self.tenant_uuid)
        except HTTPError:
            raise
        except RequestException as e:
            raise AccentConfdUnreachable(self._confd, e)

    def context(self):
        line = self._get()
        return line['context']

    def interface(self):
        line = self._get()
        protocol = line['protocol'].replace('sip', 'pjsip')
        return "{}/{}".format(protocol, line['name'])

    def interface_autoanswer(self):
        interface = self.interface()
        if interface.startswith('sccp/'):
            interface = f'{interface}/autoanswer'
        return interface

    def protocol(self):
        line = self._get()
        return line['protocol']

    def is_online(self, ari):
        line = self._get()
        name = line['name']
        tech = line['protocol']
        if tech == 'sip':
            tech = 'pjsip'

        return ari.endpoints.get(tech=tech, resource=name).json['state'] == 'online'


class Conference:
    def __init__(self, tenant_uuid, conference_id, confd_client):
        self.tenant_uuid = tenant_uuid
        self.conference_id = conference_id
        self._confd = confd_client

    def exists(self):
        try:
            conferences = self._confd.conferences.list(
                tenant_uuid=self.tenant_uuid, recurse=True
            )['items']
        except RequestException as e:
            raise AccentConfdUnreachable(self._confd, e)
        return self.conference_id in (conference['id'] for conference in conferences)

    @classmethod
    def from_id(cls, conference_id, confd_client):
        try:
            conference = confd_client.conferences.get(conference_id)
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                raise NoSuchConferenceID(conference_id)
            raise
        return cls(conference['tenant_uuid'], conference['id'], confd_client)


def get_voicemail(tenant_uuid, voicemail_id, confd_client):
    try:
        return confd_client.voicemails.get(voicemail_id, tenant_uuid=tenant_uuid)
    except HTTPError as e:
        if not_found(e):
            raise NoSuchVoicemail(voicemail_id)
        raise
    except RequestException as e:
        raise AccentConfdUnreachable(confd_client, e)


def get_user_voicemail(user_uuid, confd_client):
    try:
        voicemail = confd_client.users(user_uuid).get_voicemail()
        if not voicemail:
            raise NoSuchUserVoicemail(user_uuid)
    except HTTPError as e:
        if not_found(e):
            raise NoSuchUserVoicemail(user_uuid)
        raise
    except RequestException as e:
        raise AccentConfdUnreachable(confd_client, e)

    return voicemail
