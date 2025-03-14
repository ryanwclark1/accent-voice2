# Copyright 2023 Accent Communications

import logging
import re
import threading
from abc import abstractmethod

from accent_calld.plugin_helpers import ami
from accent_calld.plugin_helpers.ari_ import AUTO_ANSWER_VARIABLES, ARINotFound, Channel
from accent_calld.plugin_helpers.confd import User
from accent_calld.plugin_helpers.exceptions import (
    InvalidUserLine,
    InvalidUserUUID,
    NotEnoughChannels,
    TooManyChannels,
    UserPermissionDenied,
)

from .exceptions import (
    NoSuchRelocate,
    RelocateAlreadyStarted,
    RelocateCreationError,
    TooManyChannelCandidates,
)
from .relocate import Relocate

logger = logging.getLogger(__name__)


class DestinationFactory:
    def __init__(self, amid, ari):
        self.amid = amid
        self.ari = ari

    def from_type(self, type_, details, initiator_call):
        if type_ == 'interface':
            return InterfaceDestination(self.ari, details, initiator_call)
        elif type_ == 'extension':
            return ExtensionDestination(self.amid, details)
        raise NotImplementedError(type_)


class InvalidDestination(Exception):
    def __init__(self, details):
        self._details = details
        super().__init__(details)


class Destination:
    def __init__(self, details):
        self._details = details
        self.assert_is_valid()

    def assert_is_valid(self):
        if not self.is_valid():
            raise InvalidDestination(self._details)

    @abstractmethod
    def is_valid(self) -> bool:
        ...


class InterfaceDestination(Destination):
    pjsip_contact_re = re.compile(r'pjsip/[a-z0-9]+/sip:[a-z0-9]+@.*', re.IGNORECASE)

    def __init__(self, ari, details, initiator_call):
        self.ari = ari
        self.initiator_call = initiator_call

        interface = details['interface']

        if interface.startswith('pjsip/'):
            self._interface = self._get_pjsip_interface(details)
        else:
            self._interface = interface

        super().__init__(details)

    def is_valid(self):
        return True

    def ari_endpoint(self):
        return self._interface

    def _get_pjsip_interface(self, details):
        contact = details.get('contact')
        interface = details['interface']
        if not contact:
            return interface

        matches = self.pjsip_contact_re.match(contact)
        if matches:
            return contact

        _, peer_name = interface.split('/', 1)
        asterisk_dialplan_function = f'PJSIP_DIAL_CONTACTS({peer_name})'
        try:
            response = self.ari.channels.getChannelVar(
                channelId=self.initiator_call,
                variable=asterisk_dialplan_function,
            )
        except ARINotFound as e:
            msg = f'Cannot find result for {asterisk_dialplan_function} {e}'
            raise RelocateCreationError(msg, details)

        uri_start = f'PJSIP/{peer_name}/sip:{contact}'
        for contact_uri in response['value'].split('&'):
            if contact_uri.startswith(uri_start):
                return contact_uri

        raise RelocateCreationError('Failed to find a matching contact', details)


class ExtensionDestination(Destination):
    def __init__(self, amid, details):
        self._amid = amid
        self._exten = details['exten']
        self._context = details['context']
        super().__init__(details)

    def is_valid(self):
        return (
            self._exten is not None
            and self._context is not None
            and ami.extension_exists(self._amid, self._context, self._exten)
        )

    def ari_endpoint(self):
        return 'Local/{exten}@{context}'.format(
            exten=self._exten, context=self._context
        )


class RelocatesService:
    def __init__(self, amid, ari, confd_client, notifier, relocates, state_factory):
        self.ari = ari
        self.confd_client = confd_client
        self.notifier = notifier
        self.state_factory = state_factory
        self.destination_factory = DestinationFactory(amid, ari)
        self.relocates = relocates
        self.duplicate_relocate_lock = threading.Lock()

    def list_from_user(self, user_uuid):
        return [
            relocate
            for relocate in self.relocates.list()
            if relocate.initiator == user_uuid
        ]

    def get_from_user(self, relocate_uuid, user_uuid):
        try:
            return self.relocates.get(relocate_uuid, user_uuid)
        except KeyError:
            raise NoSuchRelocate(relocate_uuid)

    def create(
        self, initiator_call, destination, location, completions, timeout, relocate=None
    ):
        try:
            relocated_channel = Channel(
                initiator_call, self.ari
            ).only_connected_channel()
        except TooManyChannels as e:
            raise TooManyChannelCandidates(e.channels)
        except NotEnoughChannels:
            raise RelocateCreationError('relocated channel not found')

        initiator_channel = Channel(initiator_call, self.ari)
        if not initiator_channel.exists():
            details = {'initiator_call': initiator_call}
            raise RelocateCreationError('initiator call not found', details)

        try:
            destination = self.destination_factory.from_type(
                destination,
                location,
                initiator_channel,
            )
        except InvalidDestination:
            details = {'destination': destination, 'location': location}
            raise RelocateCreationError('invalid destination', details)

        with self.duplicate_relocate_lock:
            if self.relocates.find_by_channel(initiator_channel.id):
                raise RelocateAlreadyStarted(initiator_channel.id)

            if not relocate:
                relocate = Relocate(self.state_factory)

            relocate.relocated_channel = relocated_channel.id
            relocate.initiator_channel = initiator_channel.id
            relocate.completions = completions
            relocate.timeout = timeout
            self.relocates.add(relocate)
            self.notifier.observe(relocate)

        with relocate.locked():
            relocate.initiate(destination)

        return relocate

    def create_from_user(
        self,
        initiator_call,
        destination,
        location,
        completions,
        timeout,
        auto_answer,
        user_uuid,
    ):
        initiator_channel = Channel(initiator_call, self.ari)
        user = User(user_uuid, self.confd_client)
        variables = {}

        if initiator_channel.user() != user_uuid:
            raise UserPermissionDenied(user_uuid, {'call': initiator_call})

        tenant_uuid = initiator_channel.tenant_uuid()
        if tenant_uuid:
            variables['ACCENT_TENANT_UUID'] = tenant_uuid

        if destination == 'line':
            try:
                destination_interface = user.line(location['line_id']).interface()
            except (InvalidUserUUID, InvalidUserLine):
                raise RelocateCreationError(
                    'invalid line for user',
                    details={'user_uuid': user_uuid, 'line_id': location['line_id']},
                )
            destination = 'interface'
            location['interface'] = destination_interface
        elif destination == 'mobile':
            try:
                mobile = user.mobile_phone_number()
                line_context = user.main_line().context()
            except (InvalidUserUUID, InvalidUserLine):
                details = {'user_uuid': user_uuid}
                raise RelocateCreationError(
                    'invalid user: could not find main line', details=details
                )
            destination = 'extension'
            location = {'exten': mobile, 'context': line_context}
            variables['ACCENT_DEREFERENCED_USERUUID'] = user_uuid

        if auto_answer:
            variables.update(AUTO_ANSWER_VARIABLES)
        relocate = Relocate(self.state_factory)
        relocate.initiator = user_uuid
        relocate.recipient_variables = variables

        return self.create(
            initiator_call,
            destination,
            location,
            completions,
            timeout,
            relocate=relocate,
        )

    def complete_from_user(self, relocate_uuid, user_uuid):
        try:
            relocate = self.relocates.get(relocate_uuid, user_uuid)
        except KeyError:
            raise NoSuchRelocate(relocate_uuid)

        with relocate.locked():
            relocate.complete()

    def cancel_from_user(self, relocate_uuid, user_uuid):
        try:
            relocate = self.relocates.get(relocate_uuid, user_uuid)
        except KeyError:
            raise NoSuchRelocate(relocate_uuid)

        with relocate.locked():
            relocate.cancel()
