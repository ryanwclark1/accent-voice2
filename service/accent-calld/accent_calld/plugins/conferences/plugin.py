# Copyright 2023 Accent Communications

from __future__ import annotations

from accent_amid_client import Client as AmidClient
from accent_confd_client import Client as ConfdClient

from accent_calld.types import PluginDependencies

from .bus_consume import ConferencesBusEventHandler
from .http import (
    ConferenceRecordResource,
    ParticipantMuteResource,
    ParticipantResource,
    ParticipantsResource,
    ParticipantsUserResource,
    ParticipantUnmuteResource,
)
from .notifier import ConferencesNotifier
from .services import ConferencesService


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

        conferences_service = ConferencesService(amid_client, ari.client, confd_client)
        notifier = ConferencesNotifier(bus_publisher)
        bus_event_handler = ConferencesBusEventHandler(
            confd_client, notifier, conferences_service
        )
        bus_event_handler.subscribe(bus_consumer)

        kwargs = {'resource_class_args': [conferences_service]}
        api.add_resource(
            ParticipantsResource,
            '/conferences/<int:conference_id>/participants',
            **kwargs,
        )
        api.add_resource(
            ParticipantsUserResource,
            '/users/me/conferences/<int:conference_id>/participants',
            **kwargs,
        )
        api.add_resource(
            ParticipantResource,
            '/conferences/<int:conference_id>/participants/<participant_id>',
            **kwargs,
        )
        api.add_resource(
            ParticipantMuteResource,
            '/conferences/<int:conference_id>/participants/<participant_id>/mute',
            **kwargs,
        )
        api.add_resource(
            ParticipantUnmuteResource,
            '/conferences/<int:conference_id>/participants/<participant_id>/unmute',
            **kwargs,
        )
        api.add_resource(
            ConferenceRecordResource,
            '/conferences/<int:conference_id>/record',
            **kwargs,
        )
