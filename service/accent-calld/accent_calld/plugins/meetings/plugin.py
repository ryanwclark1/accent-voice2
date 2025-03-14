# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_amid_client import Client as AmidClient
from accent_confd_client import Client as ConfdClient

from accent_calld.types import PluginDependencies

from .bus_consume import MeetingsBusEventHandler
from .http import (
    MeetingParticipantItemResource,
    MeetingParticipantItemUserResource,
    MeetingParticipantsResource,
    MeetingParticipantsUserResource,
    MeetingStatusGuestResource,
)
from .notifier import MeetingsNotifier
from .services import MeetingsService


class Plugin:
    def load(self, dependencies: PluginDependencies) -> None:
        api = dependencies['api']
        ari = dependencies['ari']
        bus_consumer = dependencies['bus_consumer']
        bus_publisher = dependencies['bus_publisher']
        config = dependencies['config']
        token_changed_subscribe = dependencies['token_changed_subscribe']

        amid_client = AmidClient(**config['amid'])
        confd_client = ConfdClient(**config['confd'])

        token_changed_subscribe(amid_client.set_token)
        token_changed_subscribe(confd_client.set_token)

        meetings_service = MeetingsService(
            amid_client, ari.client, confd_client, config
        )
        notifier = MeetingsNotifier(bus_publisher)
        bus_event_handler = MeetingsBusEventHandler(
            confd_client, notifier, meetings_service
        )
        bus_event_handler.subscribe(bus_consumer)

        api.add_resource(
            MeetingParticipantsResource,
            '/meetings/<meeting_uuid>/participants',
            resource_class_args=[meetings_service],
        )
        api.add_resource(
            MeetingParticipantItemResource,
            '/meetings/<meeting_uuid>/participants/<participant_id>',
            resource_class_args=[meetings_service],
        )
        api.add_resource(
            MeetingParticipantsUserResource,
            '/users/me/meetings/<meeting_uuid>/participants',
            resource_class_args=[meetings_service],
        )
        api.add_resource(
            MeetingParticipantItemUserResource,
            '/users/me/meetings/<meeting_uuid>/participants/<participant_id>',
            resource_class_args=[meetings_service],
        )
        api.add_resource(
            MeetingStatusGuestResource,
            '/guests/me/meetings/<meeting_uuid>/status',
            resource_class_args=[meetings_service],
        )
