# Copyright 2023 Accent Communications

from datetime import datetime

from hamcrest import assert_that, equal_to
from accent_lib_rest_client.tests.command import RESTCommandTestCase

from ..call_logs import CallLogsCommand


class TestCallLogs(RESTCommandTestCase):
    Command = CallLogsCommand

    csvdata = (
        "Call Date,Caller,Called,Period,user Field\r\n"
        "2015-06-29T12:01:00.725871,John (1000),1234567890,0,\r\n"
    )
    resource = 'call_logs'

    def test_list(self):
        self.session.get.return_value = self.new_response(200, body=self.csvdata)

        result = self.command.list()

        self.session.get.assert_called_once_with(
            self.resource, params={}, headers={'Accept': 'text/csv'}
        )
        assert_that(result, equal_to(self.csvdata))

    def test_list_with_dates(self):
        self.session.get.return_value = self.new_response(200, body=self.csvdata)

        expected_params = {
            'start_date': '2015-01-01T12:13:14',
            'end_date': '2015-01-02T12:13:14',
        }

        self.command.list(
            start_date=datetime(2015, 1, 1, 12, 13, 14),
            end_date=datetime(2015, 1, 2, 12, 13, 14),
        )

        self.session.get.assert_called_once_with(
            self.resource, params=expected_params, headers={'Accept': 'text/csv'}
        )

    def test_when_not_200(self):
        self.session.get.return_value = self.new_response(404)

        self.assertRaisesHTTPError(self.command.list)
