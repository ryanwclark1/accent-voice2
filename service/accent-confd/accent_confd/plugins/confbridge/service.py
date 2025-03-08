# Copyright 2023 Accent Communications

from accent_dao.resources.asterisk_file import dao as asterisk_file_dao

from accent_confd.helpers.asterisk import AsteriskConfigurationService

from .notifier import build_notifier


class ConfBridgeConfigurationService(AsteriskConfigurationService):
    file_name = 'confbridge.conf'


def build_service():
    return ConfBridgeConfigurationService(asterisk_file_dao, build_notifier())
