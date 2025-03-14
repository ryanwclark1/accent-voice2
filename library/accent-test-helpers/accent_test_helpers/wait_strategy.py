# Copyright 2023 Accent Communications

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Callable

import requests

from . import until


class WaitStrategy:
    def wait(self, integration_test: Callable[..., None]) -> None:
        raise NotImplementedError()


class NoWaitStrategy(WaitStrategy):
    def wait(self, integration_test: Callable[..., None]) -> None:
        pass


class ComponentsWaitStrategy(WaitStrategy, metaclass=ABCMeta):
    @abstractmethod
    def get_status(self, integration_test: Callable[..., None]) -> dict:
        pass

    def __init__(self, components: list[str]):
        self._components = components

    def wait(self, integration_test: Callable[..., None]) -> None:
        def components_are_ok(components: list[str]) -> None:
            try:
                status = self.get_status(integration_test)
            except requests.RequestException:
                status = {}

            for component in components:
                assert status[component]['status'] == 'ok'

        until.assert_(components_are_ok, self._components, timeout=10)
