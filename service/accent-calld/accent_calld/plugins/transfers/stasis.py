# Copyright 2023 Accent Communications

import logging

from accent.pubsub import Pubsub
from accent_amid_client import Client as AmidClient
from ari.exceptions import ARINotFound, ARINotInStasis

from accent_calld.ari_ import DEFAULT_APPLICATION_NAME, ARIClientProxy, CoreARI
from accent_calld.plugin_helpers.ari_ import Channel, GlobalVariableAdapter
from accent_calld.plugin_helpers.exceptions import AccentAmidError

from . import ari_helpers
from .event import CreateTransferEvent, TransferRecipientAnsweredEvent
from .exceptions import InvalidEvent, TransferException
from .lock import HangupLock, InvalidLock
from .services import TransfersService
from .state import StateFactory
from .state_persistor import StatePersistor
from .transfer import TransferRole, TransferStatus

logger = logging.getLogger(__name__)


class TransfersStasis:
    def __init__(
        self, amid_client, ari, services, state_factory, state_persistor, accent_uuid
    ):
        self.ari: ARIClientProxy = ari.client
        self._core_ari: CoreARI = ari
        self.amid: AmidClient = amid_client
        self.services: TransfersService = services
        self.accent_uuid: str = accent_uuid
        self.stasis_start_pubsub: Pubsub = Pubsub()
        self.stasis_start_pubsub.set_exception_handler(self.invalid_event)
        self.hangup_pubsub: Pubsub = Pubsub()
        self.hangup_pubsub.set_exception_handler(self.invalid_event)
        self.state_factory: StateFactory = state_factory
        self.state_persistor: StatePersistor = state_persistor

    def initialize(self):
        self._subscribe()
        self._core_ari.register_application(DEFAULT_APPLICATION_NAME)

    def _subscribe(self):
        self.ari.on_application_registered(
            DEFAULT_APPLICATION_NAME, self.process_lost_hangups
        )
        self.ari.on_application_registered(
            DEFAULT_APPLICATION_NAME, self.process_answered_calls
        )
        self.ari.on_channel_event('ChannelEnteredBridge', self.release_hangup_lock)
        self.ari.on_channel_event(
            'ChannelDestroyed', self.bypass_hangup_lock_from_source
        )
        self.ari.on_bridge_event('BridgeDestroyed', self.clean_bridge_variables)

        self.ari.on_channel_event('ChannelLeftBridge', self.clean_bridge)

        self.ari.on_channel_event('StasisStart', self.stasis_start)
        self.stasis_start_pubsub.subscribe(
            'transfer_recipient_called', self.transfer_recipient_answered
        )
        self.stasis_start_pubsub.subscribe('create_transfer', self.create_transfer)

        self.ari.on_channel_event('ChannelDestroyed', self.hangup)
        self.ari.on_channel_event('StasisEnd', self.hangup)
        self.ari.on_channel_event('ChannelMohStop', self.moh_stop)
        self.hangup_pubsub.subscribe(TransferRole.recipient, self.recipient_hangup)
        self.hangup_pubsub.subscribe(TransferRole.initiator, self.initiator_hangup)
        self.hangup_pubsub.subscribe(TransferRole.transferred, self.transferred_hangup)

        self.ari.on_channel_event('ChannelCallerId', self.update_transfer_caller_id)

    def moh_stop(self, channel, event):
        logger.debug(
            'received ChannelMohStop for channel %s (%s)',
            channel.id,
            event['channel']['name'],
        )
        try:
            transfer = self.state_persistor.get_by_channel(channel.id)
        except KeyError:
            logger.debug(
                'ignoring ChannelMohStop event: channel %s, app %s',
                event['channel']['name'],
                event['application'],
            )
            return

        transfer_role = transfer.role(channel.id)
        if transfer_role != TransferRole.transferred:
            logger.debug(
                'ignoring ChannelMohStop event: channel %s, app %s',
                event['channel']['name'],
                event['application'],
            )
            return

        with self.state_factory.make(transfer.id) as transfer_state:
            transfer_state.transferred_moh_stop()

    def invalid_event(self, _, __, exception):
        if isinstance(exception, InvalidEvent):
            event = exception.event
            logger.error('invalid stasis event received: %s', event)
        elif isinstance(exception, AccentAmidError) or isinstance(
            exception, TransferException
        ):
            self.handle_error(exception)
        else:
            raise exception

    def handle_error(self, exception):
        logger.error('%s: %s', exception.message, exception.details)

    def process_lost_hangups(self):
        transfers = list(self.state_persistor.list())

        logger.debug('Processing lost hangups since last stop...')
        for transfer in transfers:
            with self.state_factory.make(transfer.id) as transfer_state:
                if not Channel(transfer.transferred_call, self.ari).exists():
                    logger.debug('Transferred hangup from transfer %s', transfer.id)
                    transfer_state = transfer_state.transferred_hangup()
                if not Channel(transfer.initiator_call, self.ari).exists():
                    logger.debug('Initiator hangup from transfer %s', transfer.id)
                    transfer_state = transfer_state.initiator_hangup()
                if not Channel(transfer.recipient_call, self.ari).exists():
                    logger.debug('Recipient hangup from transfer %s', transfer.id)
                    transfer_state = transfer_state.recipient_hangup()
        logger.debug('Done.')

    def process_answered_calls(self):
        transfers = list(self.state_persistor.list())

        logger.info(
            'Processing lost answered calls for %d remaining transfers since last stop...',
            len(transfers),
        )
        answered_calls = 0
        for transfer in transfers:
            with self.state_factory.make(transfer.id) as transfer_state:
                if (
                    transfer_state.name == TransferStatus.ringback
                    and Channel(transfer.recipient_call, self.ari).exists()
                ):
                    channel = self.ari.channels.get(channelId=transfer.recipient_call)
                    if channel.json['state'] != 'Up':
                        logger.debug('Recipient answered from transfer %s', transfer.id)
                        continue
                    event = {'args': ['', '', transfer.id]}
                    self.transfer_recipient_answered((channel, event))
                    answered_calls += 1
        logger.debug(
            'Finished processing %d answered calls since last stop.', answered_calls
        )

    def stasis_start(self, event_objects, event):
        try:
            sub_app, *_ = event['args']
        except ValueError:
            return

        if sub_app != 'transfer':
            return

        try:
            sub_app_transfer, transfer_action, *_ = event['args']
        except ValueError:
            logger.debug(
                'ignoring StasisStart event: channel %s, app %s, args %s',
                event['channel']['name'],
                event['application'],
                event['args'],
            )
            return

        channel = event_objects['channel']
        logger.debug('processing stasis_start from channel %s', channel.id)
        self.stasis_start_pubsub.publish(transfer_action, (channel, event))

    def hangup(self, channel, event):
        try:
            transfer = self.state_persistor.get_by_channel(channel.id)
        except KeyError:
            logger.debug(
                'ignoring StasisEnd event: channel %s, app %s',
                event['channel']['name'],
                event['application'],
            )
            return

        logger.debug('processing hangup event from channel %s', channel.id)
        transfer_role = transfer.role(channel.id)
        self.hangup_pubsub.publish(transfer_role, transfer)

    def transfer_recipient_answered(self, channel_event):
        channel, event = channel_event
        logger.debug(
            'processing transfer recipient answer event from channel %s', channel.id
        )
        event = TransferRecipientAnsweredEvent(event)

        transfer_id = event.transfer_bridge
        try:
            with self.state_factory.make(transfer_id) as transfer_state:
                logger.debug('recipient answered, transfer continues normally')
                transfer_state.recipient_answer()
        except KeyError:
            logger.debug('recipient answered, but transfer was lost')
            # avoid leaving recipient channel hanging
            channel.hangup()

    def create_transfer(self, channel_event):
        channel, event = channel_event
        logger.debug('processing create transfer event from channel %s', channel.id)
        event = CreateTransferEvent(event)
        try:
            transfer = self.state_persistor.get(event.transfer_id)
        except KeyError:
            logger.error('transfer %s was lost')
            # avoid leaving channel hanging
            channel.hangup()
            return

        transfer_role = transfer.role(channel.id)
        with self.state_factory.make(transfer.id) as transfer_state:
            if transfer_role == TransferRole.initiator:
                new_state = transfer_state.initiator_joined_stasis()
            elif transfer_role == TransferRole.transferred:
                new_state = transfer_state.transferred_joined_stasis()

            if new_state.transfer.flow == 'blind':
                new_state.complete()

    def recipient_hangup(self, transfer):
        logger.debug('recipient hangup = cancel transfer %s', transfer.id)
        with self.state_factory.make(transfer.id) as transfer_state:
            transfer_state.recipient_hangup()

    def initiator_hangup(self, transfer):
        logger.debug('initiator hangup = complete transfer %s', transfer.id)
        with self.state_factory.make(transfer.id) as transfer_state:
            transfer_state.initiator_hangup()

    def transferred_hangup(self, transfer):
        logger.debug('transferred hangup = abandon transfer %s', transfer.id)
        with self.state_factory.make(transfer.id) as transfer_state:
            transfer_state.transferred_hangup()

    def clean_bridge(self, channel, event):
        if event['application'] != 'callcontrol':
            return

        try:
            bridge = self.ari.bridges.get(bridgeId=event['bridge']['id'])
        except ARINotFound:
            return
        if bridge.json['bridge_type'] != 'mixing':
            return

        # check if bridge is associated with transfer
        # and avoid touching it if transfer is still active
        try:
            transfer_id = ari_helpers.get_bridge_variable(
                self.ari, bridge.id, 'ACCENT_TRANSFER_ID'
            )
        except ARINotFound:
            transfer_id = None

        if transfer_id:
            try:
                transfer = self.state_persistor.get(transfer_id)
            except KeyError:
                logger.debug(
                    'bridge(id=%s) has variable ACCENT_TRANSFER_ID=%s, '
                    'but transfer is not persisted anymore',
                    bridge.id,
                    transfer_id,
                )
                transfer = None

            if transfer:
                logger.debug(
                    'transfer(id=%s) in progress(status=%s) using bridge(id=%s), '
                    'leaving bridge intact',
                    transfer_id,
                    transfer.status,
                    bridge.id,
                )
                return

        logger.debug('cleaning bridge %s', bridge.id)

        if len(bridge.json['channels']) == 1:
            logger.debug('one channel left bridge %s', bridge.id)
            lone_channel_id = bridge.json['channels'][0]

            try:
                bridge_is_locked = HangupLock.from_target(self.ari, bridge.id)
            except InvalidLock:
                bridge_is_locked = False

            if not bridge_is_locked:
                logger.debug('emptying bridge %s', bridge.id)
                try:
                    self.ari.channels.hangup(channelId=lone_channel_id)
                except ARINotFound:
                    pass

        try:
            bridge = bridge.get()
        except ARINotFound:
            return
        if len(bridge.json['channels']) == 0:
            self.bypass_hangup_lock_from_target(bridge)

            logger.debug('destroying bridge %s', bridge.id)
            try:
                bridge.destroy()
            except (ARINotInStasis, ARINotFound):
                pass

    def clean_bridge_variables(self, bridge, event):
        global_variable = f'ACCENT_BRIDGE_VARIABLES_{bridge.id}'
        GlobalVariableAdapter(self.ari).unset(global_variable)

    def release_hangup_lock(self, channel, event):
        lock_source = channel
        lock_target_candidate_id = event['bridge']['id']
        try:
            lock = HangupLock(self.ari, lock_source.id, lock_target_candidate_id)
            lock.release()
        except InvalidLock:
            pass

    def bypass_hangup_lock_from_source(self, channel, event):
        lock_source = channel
        for lock in HangupLock.from_source(self.ari, lock_source.id):
            lock.kill_target()

    def bypass_hangup_lock_from_target(self, bridge):
        try:
            lock = HangupLock.from_target(self.ari, bridge.id)
            lock.kill_source()
        except InvalidLock:
            pass

    def update_transfer_caller_id(self, channel, event):
        try:
            transfer = self.state_persistor.get_by_channel(channel.id)
        except KeyError:
            logger.debug(
                'ignoring ChannelCallerId event: channel %s', event['channel']['name']
            )
            return

        transfer_role = transfer.role(channel.id)
        if transfer_role != TransferRole.recipient:
            logger.debug(
                'ignoring ChannelCallerId event: channel %s', event['channel']['name']
            )
            return

        try:
            ari_helpers.update_connectedline(
                self.ari, self.amid, transfer.initiator_call, transfer.recipient_call
            )
        except ARINotFound:
            try:
                ari_helpers.update_connectedline(
                    self.ari,
                    self.amid,
                    transfer.transferred_call,
                    transfer.recipient_call,
                )
            except ARINotFound:
                logger.debug('cannot update transfer callerid: everyone hung up')
