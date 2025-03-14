# Copyright 2023 Accent Communications

import logging

from accent_calld.plugin_helpers.confd import Conference
from accent_calld.plugin_helpers.exceptions import NoSuchConferenceID

from .schemas import participant_schema

logger = logging.getLogger(__name__)


class ConferencesBusEventHandler:
    def __init__(self, confd, notifier, service):
        self._confd = confd
        self._notifier = notifier
        self._service = service

    def subscribe(self, bus_consumer):
        bus_consumer.subscribe('ConfbridgeJoin', self._notify_participant_joined)
        bus_consumer.subscribe('ConfbridgeLeave', self._notify_participant_left)
        bus_consumer.subscribe('ConfbridgeMute', self._notify_participant_muted)
        bus_consumer.subscribe('ConfbridgeUnmute', self._notify_participant_unmuted)
        bus_consumer.subscribe('ConfbridgeRecord', self._notify_record_started)
        bus_consumer.subscribe('ConfbridgeStopRecord', self._notify_record_stopped)
        bus_consumer.subscribe('ConfbridgeTalking', self._notify_participant_talking)

    def _notify_participant_joined(self, event):
        conference_id = self._extract_conference_id(event['Conference'])
        if not conference_id:
            return

        try:
            conference = Conference.from_id(conference_id, self._confd)
        except NoSuchConferenceID:
            logger.debug(
                'Ignored participant joining conference %s: no such conference ID',
                conference_id,
            )
            return

        logger.debug('Participant joined conference %s', conference_id)
        raw_participant = {
            'id': event['Uniqueid'],
            'caller_id_name': event['CallerIDName'],
            'caller_id_number': event['CallerIDNum'],
            'muted': event['Muted'] == 'Yes',
            'answered_time': 0,
            'admin': event['Admin'] == 'Yes',
            'language': event['Language'],
            'call_id': event['Uniqueid'],
            'user_uuid': event.get('ChanVariable', {}).get('ACCENT_USERUUID'),
        }

        participant = participant_schema.load(raw_participant)

        participants_already_present = self._service.list_participants(
            conference.tenant_uuid, conference_id
        )

        self._notifier.participant_joined(
            conference.tenant_uuid,
            conference_id,
            participant,
            participants_already_present,
        )

    def _notify_participant_left(self, event):
        conference_id = self._extract_conference_id(event['Conference'])
        if not conference_id:
            return

        try:
            conference = Conference.from_id(conference_id, self._confd)
        except NoSuchConferenceID:
            logger.debug(
                'Ignored participant joining conference %s: no such conference ID',
                conference_id,
            )
            return

        logger.debug('Participant left conference %s', conference_id)
        raw_participant = {
            'id': event['Uniqueid'],
            'caller_id_name': event['CallerIDName'],
            'caller_id_number': event['CallerIDNum'],
            'muted': False,
            'answered_time': '0',
            'admin': event['Admin'] == 'Yes',
            'language': event['Language'],
            'call_id': event['Uniqueid'],
            'user_uuid': event.get('ChanVariable', {}).get('ACCENT_USERUUID'),
        }

        participant = participant_schema.load(raw_participant)

        participants_already_present = self._service.list_participants(
            conference.tenant_uuid, conference_id
        )

        self._notifier.participant_left(
            conference.tenant_uuid,
            conference_id,
            participant,
            participants_already_present,
        )

    def _notify_participant_muted(self, event):
        conference_id = self._extract_conference_id(event['Conference'])
        if not conference_id:
            return

        logger.debug('Participant in conference %s was muted', conference_id)
        raw_participant = {
            'id': event['Uniqueid'],
            'caller_id_name': event['CallerIDName'],
            'caller_id_number': event['CallerIDNum'],
            'muted': True,
            'answered_time': '0',
            'admin': event['Admin'] == 'Yes',
            'language': event['Language'],
            'call_id': event['Uniqueid'],
            'user_uuid': event.get('ChanVariable', {}).get('ACCENT_USERUUID'),
        }

        tenant_uuid = event.get('ChanVariable', {}).get('ACCENT_TENANT_UUID')
        participant = participant_schema.load(raw_participant)
        self._notifier.participant_muted(conference_id, tenant_uuid, participant)

    def _notify_participant_unmuted(self, event):
        conference_id = self._extract_conference_id(event['Conference'])
        if not conference_id:
            return

        logger.debug('Participant in conference %s was unmuted', conference_id)
        raw_participant = {
            'id': event['Uniqueid'],
            'caller_id_name': event['CallerIDName'],
            'caller_id_number': event['CallerIDNum'],
            'muted': False,
            'answered_time': '0',
            'admin': event['Admin'] == 'Yes',
            'language': event['Language'],
            'call_id': event['Uniqueid'],
            'user_uuid': event.get('ChanVariable', {}).get('ACCENT_USERUUID'),
        }

        tenant_uuid = event.get('ChanVariable', {}).get('ACCENT_TENANT_UUID')
        participant = participant_schema.load(raw_participant)
        self._notifier.participant_unmuted(conference_id, tenant_uuid, participant)

    def _notify_record_started(self, event):
        conference_id = self._extract_conference_id(event['Conference'])
        if not conference_id:
            return

        logger.debug('Conference %s is being recorded', conference_id)
        try:
            conference = Conference.from_id(conference_id, self._confd)
        except NoSuchConferenceID:
            logger.error(
                'Could not start recording for conference %s: no such conference ID',
                conference_id,
            )
            return

        self._notifier.conference_record_started(conference_id, conference.tenant_uuid)

    def _notify_record_stopped(self, event):
        conference_id = self._extract_conference_id(event['Conference'])
        if not conference_id:
            return

        logger.debug('Conference %s is not being recorded', conference_id)
        try:
            conference = Conference.from_id(conference_id, self._confd)
        except NoSuchConferenceID:
            logger.error(
                'Could not stop recording for conference %s: no such conference ID',
                conference_id,
            )
            return

        self._notifier.conference_record_stopped(conference_id, conference.tenant_uuid)

    def _notify_participant_talking(self, event):
        conference_id = self._extract_conference_id(event['Conference'])
        if not conference_id:
            return

        talking = event['TalkingStatus'] == 'on'
        logger.debug(
            'Participant in conference %s is talking: %s', conference_id, talking
        )

        raw_participant = {
            'id': event['Uniqueid'],
            'caller_id_name': event['CallerIDName'],
            'caller_id_number': event['CallerIDNum'],
            'muted': False,
            'answered_time': '0',
            'admin': event['Admin'] == 'Yes',
            'language': event['Language'],
            'call_id': event['Uniqueid'],
            'user_uuid': event.get('ChanVariable', {}).get('ACCENT_USERUUID'),
        }

        participant = participant_schema.load(raw_participant)

        conference = Conference.from_id(conference_id, self._confd)

        participants = self._service.list_participants(
            conference.tenant_uuid, conference_id
        )

        if talking:
            self._notifier.participant_talk_started(
                conference_id, conference.tenant_uuid, participant, participants
            )
        else:
            self._notifier.participant_talk_stopped(
                conference_id, conference.tenant_uuid, participant, participants
            )

    def _extract_conference_id(self, conference_name):
        try:
            return int(conference_name.rsplit('-', 1)[1])
        except Exception:
            return
