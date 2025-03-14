# Copyright 2023 Accent Communications

from __future__ import annotations

from accent.pubsub import CallbackCollector
from accent_amid_client import Client as AmidClient

from accent_calld.types import PluginDependencies

from .http import (
    UserAdhocConferenceParticipantResource,
    UserAdhocConferenceResource,
    UserAdhocConferencesResource,
)
from .notifier import AdhocConferencesNotifier
from .services import AdhocConferencesService
from .stasis import AdhocConferencesStasis


class Plugin:
    def load(self, dependencies: PluginDependencies) -> None:
        api = dependencies['api']
        ari = dependencies['ari']
        bus_publisher = dependencies['bus_publisher']
        config = dependencies['config']
        token_changed_subscribe = dependencies['token_changed_subscribe']

        amid_client = AmidClient(**config['amid'])

        token_changed_subscribe(amid_client.set_token)

        notifier = AdhocConferencesNotifier(bus_publisher)
        adhoc_conferences_service = AdhocConferencesService(
            amid_client, ari.client, notifier
        )

        startup_callback_collector = CallbackCollector()
        adhoc_conferences_stasis = AdhocConferencesStasis(ari, notifier)
        ari.client_initialized_subscribe(startup_callback_collector.new_source())
        startup_callback_collector.subscribe(adhoc_conferences_stasis.initialize)

        api.add_resource(
            UserAdhocConferencesResource,
            '/users/me/conferences/adhoc',
            resource_class_args=[adhoc_conferences_service],
        )
        api.add_resource(
            UserAdhocConferenceResource,
            '/users/me/conferences/adhoc/<adhoc_conference_id>',
            resource_class_args=[adhoc_conferences_service],
        )
        api.add_resource(
            UserAdhocConferenceParticipantResource,
            '/users/me/conferences/adhoc/<adhoc_conference_id>/participants/<call_id>',
            resource_class_args=[adhoc_conferences_service],
        )
