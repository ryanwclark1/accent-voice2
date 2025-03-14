# Copyright 2023 Accent Communications

from contextlib import contextmanager
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import sentinel as s

from hamcrest import assert_that, calling, has_properties, not_, raises

from ..bus import EventHandler
from ..services import ConfdCache, Endpoint, StatusCache


class TestBusEvent(TestCase):
    def setUp(self):
        endpoint = self.updated_endpoint = Mock(Endpoint)

        class StatusCacheMock(Mock):
            call_count = 0

            def assert_not_called(self):
                assert self.call_count == 0

            @contextmanager
            def update(self, techno, name):
                self.call_count += 1
                endpoint.techno = techno
                endpoint.name = name
                yield endpoint

        self.endpoint_status_cache = StatusCacheMock(StatusCache)
        self.confd_cache = Mock(ConfdCache)
        self.handler = EventHandler(self.endpoint_status_cache, self.confd_cache)

    def test_on_trunk_registering(self):
        self.confd_cache.get_trunk_by_username.return_value = {'name': 'foobar'}
        event = {
            'ChannelType': 'PJSIP',
            'Domain': 'sip:accent-dev-gateway.lan.accentvoice.io',
            'Event': 'Registry',
            'Privilege': 'system,all',
            'Status': 'Registered',
            'Username': 'sip:dev_370@accent-dev-gateway.lan.accentvoice.io',
        }

        self.handler.on_registry(event)

        assert_that(
            self.updated_endpoint,
            has_properties(techno='PJSIP', name='foobar', registered=True),
        )

    def test_on_misconfigured_trunk_registering_ignore_event(self):
        event = {
            'Cause': 'Registration Refused',
            'ChannelType': 'IAX2',
            'Domain': '194.146.225.32:4569',
            'Event': 'Registry',
            'Privilege': 'system,all',
            'Status': 'Rejected',
            'Username': 'trunkaccentmd6',
        }

        self.handler.on_registry(event)

        self.confd_cache.get_trunk_by_username.assert_not_called()

    def test_on_trunk_deregistering(self):
        self.confd_cache.get_trunk_by_username.return_value = {'name': 'foobar'}
        event = {
            'ChannelType': 'PJSIP',
            'Domain': 'sip:accent-dev-gateway.lan.accentvoice.io',
            'Event': 'Registry',
            'Privilege': 'system,all',
            'Status': 'Unregistered',
            'Username': 'sip:dev_370@accent-dev-gateway.lan.accentvoice.io',
        }

        self.handler.on_registry(event)

        assert_that(
            self.updated_endpoint,
            has_properties(techno='PJSIP', name='foobar', registered=False),
        )

    def test_on_trunk_dissociated_deregistering(self):
        self.confd_cache.get_trunk_by_username.return_value = None
        event = {
            'ChannelType': 'PJSIP',
            'Domain': 'sip:accent-dev-gateway.lan.accentvoice.io',
            'Event': 'Registry',
            'Privilege': 'system,all',
            'Status': 'Unregistered',
            'Username': 'sip:dev_370@accent-dev-gateway.lan.accentvoice.io',
        }

        assert_that(
            calling(self.handler.on_registry).with_args(event),
            not_(raises(Exception)),
        )

    def test_on_peer_status_pjsip_registering(self):
        event = {
            'Event': 'PeerStatus',
            'Privilege': 'system,all',
            'ChannelType': 'PJSIP',
            'Peer': 'PJSIP/ycetqvtr',
            'PeerStatus': 'Reachable',
        }

        self.handler.on_peer_status(event)

        assert_that(
            self.updated_endpoint,
            has_properties(techno='PJSIP', name='ycetqvtr', registered=True),
        )

    def test_on_peer_status_pjsip_deregistering(self):
        event = {
            'Event': 'PeerStatus',
            'Privilege': 'system,all',
            'ChannelType': 'PJSIP',
            'Peer': 'PJSIP/ycetqvtr',
            'PeerStatus': 'Unreachable',
        }

        self.handler.on_peer_status(event)

        assert_that(
            self.updated_endpoint,
            has_properties(techno='PJSIP', name='ycetqvtr', registered=False),
        )

    def test_on_hangup(self):
        event = {
            'AccountCode': '',
            'CallerIDName': 'Alice',
            'CallerIDNum': '1001',
            'Cause': '16',
            'Cause-txt': 'Normal Clearing',
            'ChanVariable': {
                'ACCENT_DEREFERENCED_USERUUID': '',
                'ACCENT_SIP_CALL_ID': '779ffe58-7bf0-456f-8475-6195b88b6655',
                'ACCENT_BASE_EXTEN': '2000',
                'ACCENT_USERUUID': '',
            },
            'Channel': 'PJSIP/dev_370-00000002',
            'ChannelState': '6',
            'ChannelStateDesc': 'Up',
            'ConnectedLineName': '<unknown>',
            'ConnectedLineNum': '<unknown>',
            'Context': 'accent-application',
            'Event': 'Hangup',
            'Exten': 's',
            'Language': 'en_US',
            'Linkedid': '1574445784.4',
            'Priority': '3',
            'Privilege': 'call,all',
            'Uniqueid': '1574445784.4',
        }

        self.handler.on_hangup(event)

        self.updated_endpoint.remove_call.assert_called_once_with('1574445784.4')
        assert_that(
            self.updated_endpoint, has_properties(techno='PJSIP', name='dev_370')
        )

    def test_on_hangup_ignores_local_channels(self):
        event = {
            'AccountCode': '',
            'CallerIDName': 'Alice',
            'CallerIDNum': '1001',
            'Cause': '16',
            'Cause-txt': 'Normal Clearing',
            'ChanVariable': {
                'ACCENT_DEREFERENCED_USERUUID': '',
                'ACCENT_SIP_CALL_ID': '779ffe58-7bf0-456f-8475-6195b88b6655',
                'ACCENT_BASE_EXTEN': '2000',
                'ACCENT_USERUUID': '',
            },
            'Channel': 'Local/1234@usersharedlines-0001',
            'ChannelState': '6',
            'ChannelStateDesc': 'Up',
            'ConnectedLineName': '<unknown>',
            'ConnectedLineNum': '<unknown>',
            'Context': 'accent-application',
            'Event': 'Hangup',
            'Exten': 's',
            'Language': 'en_US',
            'Linkedid': '1574445784.4',
            'Priority': '3',
            'Privilege': 'call,all',
            'Uniqueid': '1574445784.4',
        }

        self.handler.on_hangup(event)

        self.endpoint_status_cache.assert_not_called()

    def test_on_new_channel(self):
        event = {
            'AccountCode': '',
            'CallerIDName': 'Alice',
            'CallerIDNum': '1001',
            'ChanVariable': {
                'ACCENT_DEREFERENCED_USERUUID': '',
                'ACCENT_SIP_CALL_ID': '',
                'ACCENT_BASE_EXTEN': '',
                'ACCENT_USERUUID': '',
            },
            'Channel': 'PJSIP/dev_370-00000002',
            'ChannelState': '4',
            'ChannelStateDesc': 'Ring',
            'ConnectedLineName': '<unknown>',
            'ConnectedLineNum': '<unknown>',
            'Context': 'from-extern',
            'Event': 'Newchannel',
            'Exten': '2000',
            'Language': 'en',
            'Linkedid': '1574445784.4',
            'Priority': '1',
            'Privilege': 'call,all',
            'Uniqueid': '1574445784.4',
        }

        self.handler.on_new_channel(event)

        self.updated_endpoint.add_call.assert_called_once_with('1574445784.4')
        assert_that(
            self.updated_endpoint, has_properties(techno='PJSIP', name='dev_370')
        )

    def test_on_new_channel_ignore_local_channels(self):
        event = {
            'AccountCode': '',
            'CallerIDName': 'Alice',
            'CallerIDNum': '1001',
            'ChanVariable': {
                'ACCENT_DEREFERENCED_USERUUID': '',
                'ACCENT_SIP_CALL_ID': '',
                'ACCENT_BASE_EXTEN': '',
                'ACCENT_USERUUID': '',
            },
            'Channel': 'Local/1234@usersharedlines-0001',
            'ChannelState': '4',
            'ChannelStateDesc': 'Ring',
            'ConnectedLineName': '<unknown>',
            'ConnectedLineNum': '<unknown>',
            'Context': 'from-extern',
            'Event': 'Newchannel',
            'Exten': '2000',
            'Language': 'en',
            'Linkedid': '1574445784.4',
            'Priority': '1',
            'Privilege': 'call,all',
            'Uniqueid': '1574445784.4',
        }

        self.handler.on_new_channel(event)

        self.endpoint_status_cache.assert_not_called()

    def test_on_line_endpoint_sip_associated(self):
        line_id = 42
        tenant_uuid = '2c34c282-433e-4bb8-8d56-fec14ff7e1e9'
        name = 'the-name'
        username = 'the-username'

        event = {
            'endpoint_sip': {
                'id': 52,
                'name': name,
                'tenant_uuid': tenant_uuid,
                'auth_section_options': [['username', username]],
            },
            'line': {'id': line_id, 'tenant_uuid': tenant_uuid},
        }

        self.handler.on_line_endpoint_sip_associated(event)

        self.confd_cache.add_line.assert_called_once_with(
            'sip',
            line_id,
            name,
            username,
            tenant_uuid,
        )

    def test_on_trunk_endpoint_sip_associated(self):
        trunk_id = 42
        tenant_uuid = '2c34c282-433e-4bb8-8d56-fec14ff7e1e9'
        name = 'the-name'
        username = 'the-username'

        event = {
            'endpoint_sip': {
                'id': 45,
                'name': name,
                'tenant_uuid': tenant_uuid,
                'registration_section_options': [['client_uri', username]],
            },
            'trunk': {
                'id': trunk_id,
                'tenant_uuid': tenant_uuid,
            },
        }

        self.handler.on_trunk_endpoint_sip_associated(event)

        self.confd_cache.add_trunk.assert_called_once_with(
            'sip',
            trunk_id,
            name,
            username,
            tenant_uuid,
        )
        self.endpoint_status_cache.add_new_sip_endpoint.assert_called_once_with(
            event['endpoint_sip']['name']
        )

    def test_on_line_endpoint_sccp_associated(self):
        line_id = 42
        tenant_uuid = '2c34c282-433e-4bb8-8d56-fec14ff7e1e9'
        name = 'the-name'

        event = {
            'endpoint_sccp': {
                'id': 7,
                'tenant_uuid': tenant_uuid,
            },
            'line': {
                'id': line_id,
                'name': name,
                'tenant_uuid': tenant_uuid,
            },
        }

        self.handler.on_line_endpoint_sccp_associated(event)

        self.confd_cache.add_line.assert_called_once_with(
            'sccp',
            line_id,
            name,
            None,
            tenant_uuid,
        )

    def test_on_trunk_endpoint_iax_associated(self):
        trunk_id = 42
        tenant_uuid = '2c34c282-433e-4bb8-8d56-fec14ff7e1e9'
        name = 'the-name'

        event = {
            'endpoint_iax': {
                'id': 45,
                'name': name,
                'tenant_uuid': tenant_uuid,
            },
            'trunk': {
                'id': trunk_id,
                'tenant_uuid': tenant_uuid,
            },
        }

        self.handler.on_trunk_endpoint_iax_associated(event)

        self.confd_cache.add_trunk.assert_called_once_with(
            'iax',
            trunk_id,
            name,
            None,
            tenant_uuid,
        )
        self.endpoint_status_cache.add_new_iax_endpoint.assert_called_once_with(
            event['endpoint_iax']['name']
        )

    def test_on_line_endpoint_custom_associated(self):
        line_id = 42
        tenant_uuid = '2c34c282-433e-4bb8-8d56-fec14ff7e1e9'
        interface = 'interface'

        event = {
            'endpoint_custom': {
                'id': 45,
                'interface': interface,
                'tenant_uuid': tenant_uuid,
            },
            'line': {
                'id': line_id,
                'tenant_uuid': tenant_uuid,
            },
        }

        self.handler.on_line_endpoint_custom_associated(event)

        self.confd_cache.add_line.assert_called_once_with(
            'custom',
            line_id,
            interface,
            None,
            tenant_uuid,
        )

    def test_on_trunk_endpoint_custom_associated(self):
        trunk_id = 42
        tenant_uuid = '2c34c282-433e-4bb8-8d56-fec14ff7e1e9'
        interface = 'interface'

        event = {
            'endpoint_custom': {
                'id': 45,
                'interface': interface,
                'tenant_uuid': tenant_uuid,
            },
            'trunk': {
                'id': trunk_id,
                'tenant_uuid': tenant_uuid,
            },
        }

        self.handler.on_trunk_endpoint_custom_associated(event)

        self.confd_cache.add_trunk.assert_called_once_with(
            'custom',
            trunk_id,
            interface,
            None,
            tenant_uuid,
        )

    def test_on_line_endpoint_sip_dissociated(self):
        line_id = 42
        event = {'line': {'id': line_id}}

        self.handler.on_line_endpoint_dissociated(event)

        self.confd_cache.delete_line.assert_called_once_with(line_id)

    def test_on_line_endpoint_sccp_dissociated(self):
        line_id = 42
        event = {'line': {'id': line_id}}

        self.handler.on_line_endpoint_dissociated(event)

        self.confd_cache.delete_line.assert_called_once_with(line_id)

    def test_on_trunk_endpoint_sip_dissociated(self):
        trunk_id = 42
        event = {'trunk': {'id': trunk_id}}

        self.handler.on_trunk_endpoint_dissociated(event)

        self.confd_cache.delete_trunk.assert_called_once_with(trunk_id)

    def test_on_trunk_endpoint_iax_dissociated(self):
        trunk_id = 42
        event = {'trunk': {'id': trunk_id}}

        self.handler.on_trunk_endpoint_dissociated(event)

        self.confd_cache.delete_trunk.assert_called_once_with(trunk_id)

    def test_on_line_endpoint_custom_dissociated(self):
        line_id = 42
        event = {'line': {'id': line_id}}

        self.handler.on_line_endpoint_dissociated(event)

        self.confd_cache.delete_line.assert_called_once_with(line_id)

    def test_on_trunk_endpoint_custom_dissociated(self):
        trunk_id = 42
        event = {'trunk': {'id': trunk_id}}

        self.handler.on_trunk_endpoint_dissociated(event)

        self.confd_cache.delete_trunk.assert_called_once_with(trunk_id)

    def test_on_line_deleted(self):
        event = {'id': 42}

        self.handler.on_line_endpoint_deleted(event)

        self.confd_cache.delete_line.assert_called_once_with(42)

    def test_on_trunk_deleted(self):
        self.confd_cache.get_trunk_by_id.return_value = {
            'technology': 'sip',
            'name': 'foobar',
        }
        event = {'id': 42}

        self.handler.on_trunk_endpoint_deleted(event)

        self.confd_cache.delete_trunk.assert_called_once_with(42)
        self.confd_cache.get_trunk_by_id.assert_called_once_with(42)
        self.endpoint_status_cache.pop.assert_called_once_with('PJSIP', 'foobar')

    def test_on_line_edited(self):
        event = {
            'id': s.line_id,
            'name': s.name,
            'protocol': 'sccp',
            'tenant_uuid': s.tenant_uuid,
        }

        self.handler.on_line_edited(event)

        self.confd_cache.update_line.assert_called_once_with(
            'sccp',
            s.line_id,
            s.name,
            None,
            s.tenant_uuid,
        )

        self.confd_cache.update_line.reset_mock()

        event = {
            'id': s.line_id,
            'name': s.name,
            'protocol': 'sip',
            'tenant_uuid': s.tenant_uuid,
        }

        self.handler.on_line_edited(event)

        self.confd_cache.update_line.assert_not_called()

    def test_on_line_endpoint_sip_updated(self):
        event = {
            'id': s.endpoint_id,
            'name': s.name,
            'tenant_uuid': s.tenant_uuid,
            'auth_section_options': [['username', s.username]],
            'trunk': None,
            'line': {'id': s.line_id},
        }

        self.handler.on_endpoint_sip_updated(event)

        self.confd_cache.update_line.assert_called_once_with(
            'sip',
            s.line_id,
            s.name,
            s.username,
            s.tenant_uuid,
        )

    def test_on_trunk_endpoint_sip_updated(self):
        event = {
            'id': s.endpoint_id,
            'name': s.name,
            'tenant_uuid': s.tenant_uuid,
            'registration_section_options': [['client_uri', s.username]],
            'trunk': {'id': s.trunk_id},
            'line': None,
        }

        self.handler.on_endpoint_sip_updated(event)

        self.confd_cache.update_trunk.assert_called_once_with(
            'sip',
            s.trunk_id,
            s.name,
            s.username,
            s.tenant_uuid,
        )

    def test_on_endpoint_iax_updated(self):
        event = {
            'id': s.endpoint_id,
            'name': s.name,
            'tenant_uuid': s.tenant_uuid,
            'trunk': {'id': s.trunk_id},
            'line': None,
        }

        self.handler.on_trunk_endpoint_iax_updated(event)

        self.confd_cache.update_trunk.assert_called_once_with(
            'iax',
            s.trunk_id,
            s.name,
            None,
            s.tenant_uuid,
        )

    def test_on_trunk_endpoint_custom_updated(self):
        event = {
            'id': s.endpoint_id,
            'interface': s.interface,
            'tenant_uuid': s.tenant_uuid,
            'trunk': {'id': s.trunk_id},
            'line': None,
        }

        self.handler.on_endpoint_custom_updated(event)

        self.confd_cache.update_line.assert_not_called()
        self.confd_cache.update_trunk.assert_called_once_with(
            'custom',
            s.trunk_id,
            s.interface,
            None,
            s.tenant_uuid,
        )

    def test_on_endpoint_sip_updated_line(self):
        event = {
            'id': s.endpoint_id,
            'name': s.name,
            'tenant_uuid': s.tenant_uuid,
            'auth_section_options': [['username', s.username]],
            'trunk': None,
            'line': {'id': s.line_id},
        }

        self.handler.on_endpoint_sip_updated(event)

        self.confd_cache.update_trunk.assert_not_called()

    def test_on_endpoint_iax_updated_line(self):
        event = {
            'id': s.endpoint_id,
            'name': s.name,
            'tenant_uuid': s.tenant_uuid,
            'trunk': None,
            'line': {'id': s.line_id},
        }

        self.handler.on_trunk_endpoint_iax_updated(event)

        self.confd_cache.update_trunk.assert_not_called()

    def test_on_endpoint_custom_updated_line(self):
        event = {
            'id': s.endpoint_id,
            'interface': s.interface,
            'tenant_uuid': s.tenant_uuid,
            'trunk': None,
            'line': {'id': s.line_id},
        }

        self.handler.on_endpoint_custom_updated(event)

        self.confd_cache.update_trunk.assert_not_called()
        self.confd_cache.update_line.assert_called_once_with(
            'custom',
            s.line_id,
            s.interface,
            None,
            s.tenant_uuid,
        )
