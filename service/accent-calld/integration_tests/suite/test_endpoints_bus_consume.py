# Copyright 2023 Accent Communications

from accent_test_helpers import until
from hamcrest import assert_that, has_entries, has_item

from .helpers.ari_ import MockEndpoint
from .helpers.base import IntegrationTest
from .helpers.calld import new_call_id
from .helpers.confd import MockLine, MockTrunk
from .helpers.constants import ACCENT_UUID, VALID_TENANT
from .helpers.wait_strategy import CalldEverythingOkWaitStrategy


class TestTrunkBusConsume(IntegrationTest):
    asset = 'basic_rest'
    wait_strategy = CalldEverythingOkWaitStrategy()

    def setUp(self):
        super().setUp()
        self.amid.reset()
        self.ari.reset()
        self.confd.reset()

    def test_when_ami_hangup_then_bus_event(self):
        call_id = new_call_id()
        trunk_id = 42
        tenant_uuid = 'the_tenant_uuid'
        name = 'abcdef'

        self.ari.set_endpoints(
            MockEndpoint('PJSIP', name, 'online', channel_ids=[call_id, new_call_id()])
        )
        self.confd.set_trunks(
            MockTrunk(
                trunk_id,
                endpoint_sip={
                    'name': name,
                    'registration_section_options': [
                        ['client_uri', 'sip:the-username@hostname']
                    ],
                },
                tenant_uuid=tenant_uuid,
            )
        )

        self.restart_service('calld')

        events = self.bus.accumulator(headers={'name': 'trunk_status_updated'})
        self.reset_clients()
        self.wait_strategy.wait(self)
        self.bus.send_ami_hangup_event(call_id, channel='PJSIP/abcdef-00000001')

        def assert_function():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='trunk_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(
                            id=trunk_id,
                            technology='sip',
                            name='abcdef',
                            current_call_count=1,
                        ),
                    )
                ),
            )

        until.assert_(assert_function, tries=5)

    def test_when_ami_newchannel_then_bus_event(self):
        trunk_id = 42
        tenant_uuid = 'the_tenant_uuid'
        name = 'abcdef'

        self.ari.set_endpoints(
            MockEndpoint(
                'PJSIP',
                name,
                'online',
                channel_ids=[new_call_id(), new_call_id()],
            )
        )
        self.confd.set_trunks(
            MockTrunk(
                trunk_id,
                endpoint_sip={
                    'name': name,
                    'registration_section_options': [['client_uri', 'the-username']],
                },
                tenant_uuid=tenant_uuid,
            )
        )

        self.restart_service('calld')

        events = self.bus.accumulator(headers={'name': 'trunk_status_updated'})
        self.reset_clients()
        self.wait_strategy.wait(self)
        self.bus.send_ami_newchannel_event(
            new_call_id(), channel='PJSIP/abcdef-00000001'
        )

        def assert_function():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='trunk_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(
                            id=trunk_id,
                            technology='sip',
                            name='abcdef',
                            current_call_count=3,
                        ),
                    )
                ),
            )

        until.assert_(assert_function, tries=5)

    def test_when_ami_peerstatus_then_bus_event(self):
        trunk_id = 42
        tenant_uuid = 'the_tenant_uuid'
        name = 'abcdef'

        self.ari.set_endpoints(
            MockEndpoint('PJSIP', name, 'offline'),
        )
        self.confd.set_trunks(
            MockTrunk(
                trunk_id,
                endpoint_sip={
                    'name': name,
                    'registration_section_options': [['client_uri', 'the-username']],
                },
                tenant_uuid=tenant_uuid,
            )
        )

        self.restart_service('calld')

        events = self.bus.accumulator(headers={'name': 'trunk_status_updated'})
        self.reset_clients()
        self.wait_strategy.wait(self)
        self.bus.send_ami_peerstatus_event('PJSIP', 'PJSIP/abcdef', 'Reachable')

        def assert_registered():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='trunk_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(
                            id=trunk_id,
                            technology='sip',
                            name='abcdef',
                            registered=True,
                        ),
                    )
                ),
            )

        until.assert_(assert_registered, tries=5)

        self.bus.send_ami_peerstatus_event('PJSIP', 'PJSIP/abcdef', 'Unreachable')

        def assert_not_registered():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='trunk_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(
                            id=trunk_id,
                            technology='sip',
                            name='abcdef',
                            registered=False,
                        ),
                    )
                ),
            )

        until.assert_(assert_not_registered, tries=5)

    def test_when_ami_registry_then_bus_event(self):
        trunk_id = 42
        tenant_uuid = 'the_tenant_uuid'
        name = 'abcdef'
        client_uri = 'sip:the-username@hostname'

        self.ari.set_endpoints(
            MockEndpoint('PJSIP', name, 'offline'),
        )
        self.confd.set_trunks(
            MockTrunk(
                trunk_id,
                endpoint_sip={
                    'name': name,
                    'registration_section_options': [['client_uri', client_uri]],
                },
                tenant_uuid=tenant_uuid,
            )
        )

        self.restart_service('calld')

        events = self.bus.accumulator(headers={'name': 'trunk_status_updated'})
        self.reset_clients()
        self.wait_strategy.wait(self)
        self.bus.send_ami_registry_event(
            'PJSIP',
            'sip:here',
            'Registered',
            client_uri,
        )

        def assert_registered():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='trunk_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(
                            id=trunk_id,
                            technology='sip',
                            name='abcdef',
                            registered=True,
                        ),
                    )
                ),
            )

        until.assert_(assert_registered, tries=5)

        self.bus.send_ami_registry_event(
            'PJSIP',
            'sip:here',
            'Unregistered',
            client_uri,
        )

        def assert_not_registered():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='trunk_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(
                            id=trunk_id,
                            technology='sip',
                            name='abcdef',
                            registered=False,
                        ),
                    )
                ),
            )

        until.assert_(assert_not_registered, tries=5)

    def test_when_trunk_associated_events_can_be_published(self):
        trunk_id = 42
        tenant_uuid = VALID_TENANT
        name = 'abcdef'
        client_uri = 'sip:the-username@hostname'

        self.ari.set_endpoints(
            MockEndpoint('PJSIP', name, 'offline', channel_ids=[]),
        )
        # There are no trunks when starting calld
        self.restart_service('calld')

        events = self.bus.accumulator(headers={'name': 'trunk_status_updated'})
        self.reset_clients()
        self.wait_strategy.wait(self)
        # A trunk is created
        self.confd.set_trunks(
            MockTrunk(
                trunk_id,
                endpoint_sip={
                    'name': name,
                    'registration_section_options': [['client_uri', client_uri]],
                },
                tenant_uuid=tenant_uuid,
            )
        )
        self.bus.send_trunk_endpoint_associated_event(trunk_id, endpoint_id=3)

        def trunk_exists():
            expected = {
                'id': trunk_id,
                'name': name,
                'technology': 'sip',
                'registered': False,
                'current_call_count': 0,
            }
            assert (
                expected
                in self.calld_client.trunks.list_trunks(tenant_uuid=tenant_uuid)[
                    'items'
                ]
            )

        until.assert_(trunk_exists, timeout=5)

        self.bus.send_ami_registry_event(
            'PJSIP',
            'sip:here',
            'Registered',
            client_uri,
        )

        def assert_function():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='trunk_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(id=trunk_id),
                    )
                ),
            )

        until.assert_(assert_function, tries=5)

        def trunk_registered():
            expected = {
                'id': trunk_id,
                'name': name,
                'technology': 'sip',
                'registered': True,
                'current_call_count': 0,
            }
            assert (
                expected
                in self.calld_client.trunks.list_trunks(tenant_uuid=tenant_uuid)[
                    'items'
                ]
            )

        until.assert_(trunk_registered, timeout=5)


class TestLineBusConsume(IntegrationTest):
    asset = 'basic_rest'
    wait_strategy = CalldEverythingOkWaitStrategy()

    def setUp(self):
        super().setUp()
        self.amid.reset()
        self.ari.reset()
        self.confd.reset()

    def test_when_ami_hangup_then_bus_event(self):
        call_id = new_call_id()
        line_id = 42
        tenant_uuid = 'the_tenant_uuid'
        name = 'abcdef'

        self.ari.set_endpoints(
            MockEndpoint('PJSIP', name, 'online', channel_ids=[call_id, new_call_id()])
        )
        self.confd.set_lines(
            MockLine(
                line_id,
                name=name,
                protocol='sip',
                endpoint_sip={
                    'name': name,
                    'auth_section_options': [['username', 'the-username']],
                },
                tenant_uuid=tenant_uuid,
            )
        )

        self.restart_service('calld')

        events = self.bus.accumulator(headers={'name': 'line_status_updated'})
        self.reset_clients()
        self.wait_strategy.wait(self)
        self.bus.send_ami_hangup_event(call_id, channel='PJSIP/abcdef-00000001')

        def assert_function():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='line_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(
                            id=line_id,
                            technology='sip',
                            name='abcdef',
                            current_call_count=1,
                        ),
                    )
                ),
            )

        until.assert_(assert_function, tries=5)

    def test_when_ami_newchannel_then_bus_event(self):
        line_id = 42
        tenant_uuid = 'the_tenant_uuid'
        name = 'abcdef'

        self.ari.set_endpoints(
            MockEndpoint(
                'PJSIP',
                name,
                'online',
                channel_ids=[new_call_id(), new_call_id()],
            )
        )
        self.confd.set_lines(
            MockLine(
                line_id,
                name=name,
                protocol='sip',
                endpoint_sip={
                    'name': name,
                    'auth_section_options': [['username', 'the-username']],
                },
                tenant_uuid=tenant_uuid,
            )
        )

        self.restart_service('calld')

        events = self.bus.accumulator(headers={'name': 'line_status_updated'})
        self.reset_clients()
        self.wait_strategy.wait(self)
        self.bus.send_ami_newchannel_event(
            new_call_id(), channel='PJSIP/abcdef-00000001'
        )

        def assert_function():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='line_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(
                            id=line_id,
                            technology='sip',
                            name='abcdef',
                            current_call_count=3,
                        ),
                    )
                ),
            )

        until.assert_(assert_function, tries=5)

    def test_when_ami_peerstatus_then_bus_event(self):
        line_id = 42
        tenant_uuid = 'the_tenant_uuid'
        name = 'abcdef'

        self.ari.set_endpoints(
            MockEndpoint('PJSIP', name, 'offline'),
        )
        self.confd.set_lines(
            MockLine(
                line_id,
                name=name,
                protocol='sip',
                endpoint_sip={
                    'name': name,
                    'auth_section_options': [['username', 'the-username']],
                },
                tenant_uuid=tenant_uuid,
            )
        )

        self.restart_service('calld')

        events = self.bus.accumulator(headers={'name': 'line_status_updated'})
        self.reset_clients()
        self.wait_strategy.wait(self)
        self.bus.send_ami_peerstatus_event('PJSIP', 'PJSIP/abcdef', 'Reachable')

        def assert_registered():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='line_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(
                            id=line_id,
                            technology='sip',
                            name='abcdef',
                            registered=True,
                        ),
                    )
                ),
            )

        until.assert_(assert_registered, tries=5)

        self.bus.send_ami_peerstatus_event('PJSIP', 'PJSIP/abcdef', 'Unreachable')

        def assert_not_registered():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='line_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(
                            id=line_id,
                            technology='sip',
                            name='abcdef',
                            registered=False,
                        ),
                    )
                ),
            )

        until.assert_(assert_not_registered, tries=5)

    def test_when_line_associated_events_can_be_published(self):
        line_id = 42
        tenant_uuid = VALID_TENANT
        name = 'abcdef'

        events = self.bus.accumulator(headers={'name': 'line_status_updated'})
        # A line is created
        self.confd.set_lines(
            MockLine(
                line_id,
                name=name,
                protocol='sip',
                endpoint_sip={
                    'name': name,
                    'auth_section_options': [['username', name]],
                },
                tenant_uuid=tenant_uuid,
            )
        )
        self.bus.send_line_endpoint_sip_associated_event(
            tenant_uuid, line_id, endpoint_id=3, endpoint_name=name
        )

        def line_exists():
            expected = {
                'id': line_id,
                'name': name,
                'technology': 'sip',
                'registered': False,
                'current_call_count': 0,
            }
            assert (
                expected
                in self.calld_client.lines.list_lines(tenant_uuid=tenant_uuid)['items']
            )

        until.assert_(line_exists, timeout=5)

        self.bus.send_ami_peerstatus_event('PJSIP', 'PJSIP/abcdef', 'Reachable')

        def assert_function():
            assert_that(
                events.accumulate(),
                has_item(
                    has_entries(
                        name='line_status_updated',
                        origin_uuid=ACCENT_UUID,
                        data=has_entries(id=line_id, registered=True),
                    )
                ),
            )

        until.assert_(assert_function, timeout=5)

        def line_registered():
            expected = {
                'id': line_id,
                'name': name,
                'technology': 'sip',
                'registered': True,
                'current_call_count': 0,
            }
            assert (
                expected
                in self.calld_client.lines.list_lines(tenant_uuid=tenant_uuid)['items']
            )

        until.assert_(line_registered, timeout=5)
