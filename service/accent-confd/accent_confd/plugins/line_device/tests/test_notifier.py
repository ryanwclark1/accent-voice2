# Copyright 2023 Accent Communications

import unittest
import uuid
from unittest.mock import Mock

from accent_bus.resources.line_device.event import (
    LineDeviceAssociatedEvent,
    LineDeviceDissociatedEvent,
)
from accent_dao.alchemy.linefeatures import LineFeatures as Line
from hamcrest import assert_that, equal_to

from accent_confd.plugins.device.model import Device

from ..notifier import LineDeviceNotifier


class TestLineDeviceNotifier(unittest.TestCase):
    REQUEST_HANDLERS = {'ipbx': ['module reload chan_sccp.so']}

    def setUp(self):
        self.sysconfd = Mock()
        self.line = Mock(
            Line,
            id=1,
            endpoint_sip={'uuid': str(uuid.uuid4())},
            endpoint_sccp=None,
            endpoint_custom=None,
            endpoint_sip_uuid=None,
            endpoint_sccp_id=None,
            endpoint_custom_id=None,
            tenant_uuid=uuid.uuid4(),
        )
        self.line.name = 'limitation of mock instantiation with name ...'
        self.device = Mock(Device, id='custom-id')
        self.bus = Mock()
        self.expected_headers = {'tenant_uuid': str(self.line.tenant_uuid)}
        self.notifier = LineDeviceNotifier(self.bus, self.sysconfd)

    def test_given_line_is_not_sccp_when_associated_then_sccp_not_reloaded(self):
        self.line.endpoint_sip_uuid = 1
        self.notifier.associated(self.line, self.device)

        assert_that(self.sysconfd.exec_request_handlers.call_count, equal_to(0))

    def test_given_line_is_not_sccp_when_dissociated_then_sccp_not_reloaded(self):
        self.line.endpoint_sip_uuid = 1
        self.notifier.dissociated(self.line, self.device)

        assert_that(self.sysconfd.exec_request_handlers.call_count, equal_to(0))

    def test_given_line_is_sccp_when_associated_then_sccp_reloaded(self):
        self.line.endpoint_sccp_id = 1
        self.notifier.associated(self.line, self.device)

        self.sysconfd.exec_request_handlers.assert_called_once_with(
            self.REQUEST_HANDLERS
        )

    def test_given_line_is_sccp_when_dissociated_then_sccp_reloaded(self):
        self.line.endpoint_sccp_id = 1
        self.notifier.dissociated(self.line, self.device)

        self.sysconfd.exec_request_handlers.assert_called_once_with(
            self.REQUEST_HANDLERS
        )

    def test_associate_then_bus_event(self):
        expected_event = LineDeviceAssociatedEvent(
            {
                'id': self.line.id,
                'name': self.line.name,
                'endpoint_sip': self.line.endpoint_sip,
                'endpoint_sccp': self.line.endpoint_sccp,
                'endpoint_custom': self.line.endpoint_custom,
            },
            {'id': self.device.id},
            self.line.tenant_uuid,
        )

        self.notifier.associated(self.line, self.device)

        self.bus.queue_event.assert_called_once_with(expected_event)

    def test_dissociate_then_bus_event(self):
        expected_event = LineDeviceDissociatedEvent(
            {
                'id': self.line.id,
                'name': self.line.name,
                'endpoint_sip': self.line.endpoint_sip,
                'endpoint_sccp': self.line.endpoint_sccp,
                'endpoint_custom': self.line.endpoint_custom,
            },
            {'id': self.device.id},
            self.line.tenant_uuid,
        )

        self.notifier.dissociated(self.line, self.device)

        self.bus.queue_event.assert_called_once_with(expected_event)
