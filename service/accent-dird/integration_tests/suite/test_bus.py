# Copyright 2023 Accent Communications

from accent_test_helpers import until
from accent_test_helpers.bus import BusClient
from hamcrest import assert_that, has_entries, has_entry, has_item

from .helpers.base import BaseDirdIntegrationTest


class TestBusConsumer(BaseDirdIntegrationTest):
    asset = 'all_routes'

    def setUp(self):
        super().setUp()
        until.true(self.bus_is_up, tries=10)
        bus_port = self.service_port(5672, 'rabbitmq')
        self.bus = BusClient.from_connection_fields(
            host='127.0.0.1',
            port=bus_port,
            exchange_name='accent-headers',
            exchange_type='headers',
        )

    def test_message_is_received(self):
        bus_events = self.bus.accumulator(headers={'name': 'dird_pong'})

        ping_event = {'name': 'dird_ping', 'data': {'payload': 'ping'}}

        self.bus.publish(
            ping_event,
            headers={'name': 'dird_ping'},
        )

        def pong_bus_event_received():
            assert_that(
                bus_events.accumulate(with_headers=True),
                has_item(
                    has_entries(
                        message=has_entries(
                            data=has_entries(
                                payload='pong',
                            ),
                        ),
                        headers=has_entry('name', 'dird_pong'),
                    )
                ),
            )

        until.assert_(pong_bus_event_received, tries=5)

    def test_message_is_received_after_error(self):
        bus_events = self.bus.accumulator(headers={'name': 'dird_pong'})

        crash_event = {'name': 'crash_ping', 'data': {'payload': 'ping'}}
        self.bus.publish(
            crash_event,
            headers={'name': 'crash_ping'},
        )

        ping_event = {'name': 'dird_ping', 'data': {'payload': 'ping'}}
        self.bus.publish(
            ping_event,
            headers={'name': 'dird_ping'},
        )

        def pong_bus_event_received():
            assert_that(
                bus_events.accumulate(with_headers=True),
                has_item(
                    has_entries(
                        message=has_entries(
                            data=has_entries(
                                payload='pong',
                            ),
                        ),
                        headers=has_entry('name', 'dird_pong'),
                    )
                ),
            )

        until.assert_(pong_bus_event_received, tries=5)
