#!/usr/bin/env python
# Copyright 2023 Accent Communications


from setuptools import find_packages, setup

setup(
    name='foo and bar service auth plugin',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'accent_auth.external_auth': [
            'foo = external_auth_service_plugin.plugin:FooPlugin',
            'bar = external_auth_service_plugin.plugin:BarPlugin',
        ]
    },
)
