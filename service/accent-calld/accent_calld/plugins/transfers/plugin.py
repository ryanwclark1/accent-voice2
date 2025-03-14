# Copyright 2023 Accent Communications

from __future__ import annotations

from accent.pubsub import CallbackCollector
from accent_amid_client import Client as AmidClient
from accent_confd_client import Client as ConfdClient

from accent_calld.types import PluginDependencies

from .http import (
    TransferCompleteResource,
    TransferResource,
    TransfersResource,
    UserTransferCompleteResource,
    UserTransferResource,
    UserTransfersResource,
)
from .notifier import TransferNotifier
from .services import TransfersService
from .stasis import TransfersStasis
from .state import state_factory
from .state_persistor import StatePersistor
from .transfer_lock import TransferLock


class Plugin:
    def load(self, dependencies: PluginDependencies) -> None:
        api = dependencies['api']
        ari = dependencies['ari']
        bus_publisher = dependencies['bus_publisher']
        config = dependencies['config']
        token_changed_subscribe = dependencies['token_changed_subscribe']

        amid_client = AmidClient(**config['amid'])
        confd_client = ConfdClient(**config['confd'])

        token_changed_subscribe(amid_client.set_token)
        token_changed_subscribe(confd_client.set_token)

        state_persistor = StatePersistor(ari.client)
        transfer_lock = TransferLock()

        notifier = TransferNotifier(bus_publisher)

        transfers_service = TransfersService(
            amid_client,
            ari.client,
            confd_client,
            notifier,
            state_factory,
            state_persistor,
            transfer_lock,
        )

        transfers_stasis = TransfersStasis(
            amid_client,
            ari,
            transfers_service,
            state_factory,
            state_persistor,
            config['uuid'],
        )

        startup_callback_collector = CallbackCollector()
        ari.client_initialized_subscribe(startup_callback_collector.new_source())
        startup_callback_collector.subscribe(transfers_stasis.initialize)

        state_factory.set_state_persistor(state_persistor)
        state_factory.set_dependencies(
            amid_client,
            ari.client,
            notifier,
            transfers_service,
            state_persistor,
            transfer_lock,
        )

        kwargs = {'resource_class_args': [transfers_service]}
        api.add_resource(TransfersResource, '/transfers', **kwargs)
        api.add_resource(TransferResource, '/transfers/<transfer_id>', **kwargs)
        api.add_resource(
            TransferCompleteResource, '/transfers/<transfer_id>/complete', **kwargs
        )
        api.add_resource(UserTransfersResource, '/users/me/transfers', **kwargs)
        api.add_resource(
            UserTransferResource, '/users/me/transfers/<transfer_id>', **kwargs
        )
        api.add_resource(
            UserTransferCompleteResource,
            '/users/me/transfers/<transfer_id>/complete',
            **kwargs,
        )
