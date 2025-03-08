#!/usr/bin/env python
# Copyright 2023 Accent Communications


from setuptools import find_packages, setup

setup(
    name='testing internal token metadata auth plugin',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'accent_auth.metadata': [
            'internal_token = metadata_internal_token.plugin:Plugin',
        ]
    },
)
