# Copyright 2023 Accent Communications

try:
    from accent_provd.plugins import StandardPlugin
    from accent_provd.servers.http import HTTPNoListingFileService
    from accent_provd.servers.tftp.service import TFTPFileService
except ImportError:
        from provd.plugins import StandardPlugin
    from provd.servers.http import HTTPNoListingFileService
    from provd.servers.tftp.service import TFTPFileService


class ZeroPlugin(StandardPlugin):
    IS_PLUGIN = True

    def __init__(self, app, plugin_dir, gen_cfg, spec_cfg):
        super().__init__(app, plugin_dir, gen_cfg, spec_cfg)
        self.tftp_service = TFTPFileService(self._tftpboot_dir)
        self.http_service = HTTPNoListingFileService(self._tftpboot_dir)
