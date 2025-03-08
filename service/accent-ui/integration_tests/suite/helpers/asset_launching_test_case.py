# Copyright 2023 Accent Communications

from accent_test_helpers.asset_launching_test_case import AssetLaunchingTestCase

from .pages.browser import RemoteBrowser
from .pages.page import Page


class AdminUIAssetLaunchingTestCase(AssetLaunchingTestCase):
    service = 'accent-ui'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            cls.browser = cls.setup_browser()
            cls.browser.start()
        except Exception:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.browser.stop()
        super().tearDownClass()

    @classmethod
    def setup_browser(cls):
        username = 'accent-auth-mock-doesnt-care-about-username'
        password = 'accent-auth-mock-doesnt-care-about-password'
        Page.CONFIG['base_url'] = 'http://ui:9296'

        browser_port = cls.service_port(4444, 'browser')
        remote_url = f'http://127.0.0.1:{browser_port}/wd/hub'
        browser = RemoteBrowser(remote_url, username, password)
        return browser
