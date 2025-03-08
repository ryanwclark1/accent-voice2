# Copyright 2023 Accent Communications

try:
    from accent_provd.plugins import Plugin
    from accent_provd.servers.tftp.service import TFTPNullService
except ImportError:
        from provd.plugins import Plugin
    from provd.servers.tftp.service import TFTPNullService

from twisted.web.resource import NoResource

_MSG = 'Null plugin always reject requests'


class NullPlugin(Plugin):
    IS_PLUGIN = True

    http_service = NoResource(_MSG)
    tftp_service = TFTPNullService(errmsg=_MSG)
