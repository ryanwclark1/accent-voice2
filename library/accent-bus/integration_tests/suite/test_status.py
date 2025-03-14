# Copyright 2023 Accent Communications

from accent_test_helpers import until
from hamcrest import assert_that, calling, has_entry, has_item, raises
from kombu.exceptions import OperationalError

from .helpers.base import BusIntegrationTest
from .helpers.events import MockEvent


class TestStatus(BusIntegrationTest):
    asset = "headers"

    def check_is_running(self):
        remote_status = self.remote_bus.get_status()
        return self.local_bus.consumer_connected() and remote_status["running"]

    def test_status_when_all_ok(self) -> None:
        until.true(self.check_is_running, tries=3)

    def test_status_when_rabbitmq_restarts(self) -> None:
        self.stop_rabbitmq()
        until.false(self.check_is_running, timeout=30)
        self.start_rabbitmq()
        until.true(self.check_is_running, timeout=30)

    def test_status_when_service_restart(self) -> None:
        self.reset_clients()
        until.true(self.check_is_running, tries=3)

    def test_publish_timeout_when_rabbitmq_is_down_then_up(self) -> None:
        event = MockEvent("some_event", value="some_value")

        self.stop_rabbitmq()

        with self.local_event(event.name):
            assert_that(
                calling(self.local_bus.publish).with_args(event),
                raises(OperationalError),
            )

            self.start_rabbitmq()
            until.true(self.check_is_running, timeout=30)

            self.local_bus.publish(event)
            assert_that(
                self.local_messages(event.name, 1),
                has_item(has_entry("value", "some_value")),
            )
