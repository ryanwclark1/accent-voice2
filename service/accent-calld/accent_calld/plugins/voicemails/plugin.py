# Copyright 2023 Accent Communications

from __future__ import annotations

import logging

from accent.status import Status
from accent_confd_client import Client as ConfdClient

from accent_calld.types import PluginDependencies, StatusDict

from .bus_consume import VoicemailsBusEventHandler
from .http import (
    UserVoicemailFolderResource,
    UserVoicemailGreetingCopyResource,
    UserVoicemailGreetingResource,
    UserVoicemailMessageResource,
    UserVoicemailRecordingResource,
    UserVoicemailResource,
    VoicemailFolderResource,
    VoicemailGreetingCopyResource,
    VoicemailGreetingResource,
    VoicemailMessageResource,
    VoicemailRecordingResource,
    VoicemailResource,
)
from .notifier import VoicemailsNotifier
from .services import VoicemailsService
from .storage import new_cache, new_filesystem_storage

logger = logging.getLogger(__name__)


class Plugin:
    def load(self, dependencies: PluginDependencies) -> None:
        api = dependencies['api']
        ari = dependencies['ari']
        bus_consumer = dependencies['bus_consumer']
        bus_publisher = dependencies['bus_publisher']
        config = dependencies['config']
        status_aggregator = dependencies['status_aggregator']
        token_changed_subscribe = dependencies['token_changed_subscribe']

        confd_client = ConfdClient(**config['confd'])

        notifier = VoicemailsNotifier(bus_publisher)

        token_changed_subscribe(confd_client.set_token)

        voicemail_storage = new_filesystem_storage()
        self._voicemail_cache = new_cache(voicemail_storage)
        try:
            self._voicemail_cache.refresh_cache()
        except Exception:
            logger.exception('fail to refresh voicemail cache')
        voicemails_service = VoicemailsService(
            ari.client, confd_client, voicemail_storage
        )

        voicemails_bus_event_handler = VoicemailsBusEventHandler(
            confd_client, notifier, self._voicemail_cache
        )
        voicemails_bus_event_handler.subscribe(bus_consumer)

        status_aggregator.add_provider(self._provide_status)

        api.add_resource(
            VoicemailResource,
            '/voicemails/<voicemail_id>',
            resource_class_args=[voicemails_service],
        )
        api.add_resource(
            VoicemailFolderResource,
            '/voicemails/<voicemail_id>/folders/<folder_id>',
            resource_class_args=[voicemails_service],
        )
        api.add_resource(
            VoicemailGreetingResource,
            '/voicemails/<voicemail_id>/greetings/<greeting>',
            resource_class_args=[voicemails_service],
        )
        api.add_resource(
            VoicemailGreetingCopyResource,
            '/voicemails/<voicemail_id>/greetings/<greeting>/copy',
            resource_class_args=[voicemails_service],
        )
        api.add_resource(
            VoicemailMessageResource,
            '/voicemails/<voicemail_id>/messages/<message_id>',
            resource_class_args=[voicemails_service],
        )
        api.add_resource(
            VoicemailRecordingResource,
            '/voicemails/<voicemail_id>/messages/<message_id>/recording',
            resource_class_args=[voicemails_service],
        )

        api.add_resource(
            UserVoicemailResource,
            '/users/me/voicemails',
            resource_class_args=[voicemails_service],
        )
        api.add_resource(
            UserVoicemailFolderResource,
            '/users/me/voicemails/folders/<folder_id>',
            resource_class_args=[voicemails_service],
        )
        api.add_resource(
            UserVoicemailGreetingResource,
            '/users/me/voicemails/greetings/<greeting>',
            resource_class_args=[voicemails_service],
        )
        api.add_resource(
            UserVoicemailGreetingCopyResource,
            '/users/me/voicemails/greetings/<greeting>/copy',
            resource_class_args=[voicemails_service],
        )
        api.add_resource(
            UserVoicemailMessageResource,
            '/users/me/voicemails/messages/<message_id>',
            resource_class_args=[voicemails_service],
        )
        api.add_resource(
            UserVoicemailRecordingResource,
            '/users/me/voicemails/messages/<message_id>/recording',
            resource_class_args=[voicemails_service],
        )

    def _provide_status(self, status: StatusDict) -> None:
        status['plugins']['voicemails']['status'] = Status.ok
        status['plugins']['voicemails']['cache_items'] = len(self._voicemail_cache)
