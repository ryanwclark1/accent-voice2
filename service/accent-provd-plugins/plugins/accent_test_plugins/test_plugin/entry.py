# Copyright 2023 Accent Communications

from accent_provd.plugins import FetchfwPluginHelper, StandardPlugin
from accent_provd.servers.tftp.service import TFTPNullService
from twisted.internet import defer
from twisted.web.resource import NoResource

_MSG = 'Test plugin for integration tests'


class TestPlugin(StandardPlugin):
    IS_PLUGIN = True

    http_service = NoResource(_MSG)
    tftp_service = TFTPNullService(errmsg=_MSG)

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        StandardPlugin.__init__(self, app, plugin_dir, gen_cfg, spec_cfg)

        downloaders = FetchfwPluginHelper.new_downloaders(gen_cfg.get('proxies'))
        fetchfw_helper = FetchfwPluginHelper(plugin_dir, downloaders)

        self.services = fetchfw_helper.services()

    def synchronize(self, device, raw_config):
        return defer.succeed(None)
