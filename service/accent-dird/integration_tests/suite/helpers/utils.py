# Copyright 2023 Accent Communications

import logging
import os
import random
import string
import uuid

import requests
from stevedore import DriverManager

from accent_dird import BaseSourcePlugin

from .constants import ASSET_ROOT

logger = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings()


def absolute_file_name(asset_name, path):
    dirname, basename = os.path.split(path)
    real_basename = f'asset.{asset_name}.{basename}'
    return os.path.join(ASSET_ROOT, dirname, real_basename)


class BackendWrapper(BaseSourcePlugin):
    def __init__(self, backend, dependencies):
        manager = DriverManager(
            namespace='accent_dird.backends', name=backend, invoke_on_load=True
        )
        self._source = manager.driver
        self._dependencies = dependencies
        self.load()

    def unload(self):
        self._source.unload()

    def load(self):
        return self._source.load(self._dependencies)

    def search(self, term, *args, **kwargs):
        return [r.fields for r in self.search_raw(term, *args, **kwargs)]

    def search_raw(self, term, *args, **kwargs):
        return self._source.search(term, *args, **kwargs)

    def first(self, term, *args, **kwargs):
        return self._source.first_match(term, *args, **kwargs).fields

    def first_match(self, exten, args=None):
        return self._source.first_match(exten, args)

    def match_all(self, terms, *args, **kwargs):
        results = self._source.match_all(terms, *args, **kwargs)
        return [value.fields for value in results.values()]

    def list(self, source_ids, *args, **kwargs):
        results = self._source.list(source_ids, *args, **kwargs)
        return [r.fields for r in results]


def new_uuid() -> str:
    return str(uuid.uuid4())


def random_string(n: int) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))
