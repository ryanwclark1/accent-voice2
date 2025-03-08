# Copyright 2023 Accent Communications

from hamcrest import assert_that, contains_exactly, contains_inanyorder, empty

from accent_dao import phone_access_dao
from accent_dao.tests.test_dao import DAOTestCase


class TestPhoneAccessDao(DAOTestCase):

    def test_get_authorized_subnets(self):
        host = '169.254.0.0/16'
        self.add_accessfeatures(host)

        hosts = phone_access_dao.get_authorized_subnets()

        assert_that(hosts, contains_exactly(host))

    def test_get_authorized_subnets_with_commented(self):
        host = '169.254.0.0/16'
        commented = 1
        self.add_accessfeatures(host, commented=commented)

        hosts = phone_access_dao.get_authorized_subnets()

        assert_that(hosts, empty())

    def test_get_authorized_subnets_multiple_results(self):
        hosts = ['169.254.0.0/16', '192.168.1.1']

        for host in hosts:
            self.add_accessfeatures(host)

        hosts = phone_access_dao.get_authorized_subnets()

        assert_that(hosts, contains_inanyorder(*hosts))
