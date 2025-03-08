# Copyright 2023 Accent Communications

from selenium.webdriver.common.by import By

from .page import Page


class IndexPage(Page):
    PATH = "/"

    def go(self):
        url = self.build_url(self.PATH)
        self.driver.get(url)
        self.wait_for(By.CLASS_NAME, 'user-header')
        return self
