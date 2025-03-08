# Copyright 2023 Accent Communications

import contextlib
from functools import wraps

from accent_dird import exception

from ..utils import new_uuid, random_string


def display(**display_args):
    display_args.setdefault('name', random_string(16))
    display_args.setdefault('tenant_uuid', new_uuid())
    display_args.setdefault('columns', [])

    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            display = self.display_crud.create(**display_args)
            try:
                result = decorated(self, display, *args, **kwargs)
            finally:
                with contextlib.suppress(exception.NoSuchDisplay):
                    self.display_crud.delete(None, display['uuid'])
            return result

        return wrapper

    return decorator


def profile(**profile_args):
    profile_args.setdefault('name', random_string(10))
    profile_args.setdefault('tenant_uuid', new_uuid())
    profile_args.setdefault('services', {})
    profile_args.setdefault('display', None)

    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            profile = self.profile_crud.create(profile_args)
            try:
                result = decorated(self, profile, *args, **kwargs)
            finally:
                with contextlib.suppress(exception.NoSuchProfileAPIException):
                    self.profile_crud.delete(None, profile['uuid'])
            return result

        return wrapper

    return decorator


def source(**source_args):
    source_args.setdefault('backend', 'csv')
    source_args.setdefault('tenant_uuid', new_uuid())
    source_args.setdefault('name', random_string(10))
    source_args.setdefault('searched_columns', [])
    source_args.setdefault('first_matched_columns', [])
    source_args.setdefault('format_columns', {})
    backend = source_args.pop('backend')

    def decorator(decorated):
        @wraps(decorated)
        def wrapper(self, *args, **kwargs):
            source = self.source_crud.create(backend, source_args)
            try:
                result = decorated(self, source, *args, **kwargs)
            finally:
                with contextlib.suppress(exception.NoSuchSource):
                    self.source_crud.delete(backend, source['uuid'], visible_tenants=None)
            return result

        return wrapper

    return decorator
