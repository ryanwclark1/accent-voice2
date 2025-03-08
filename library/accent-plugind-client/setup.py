#!/usr/bin/env python3
# Copyright 2023 Accent Communications

from setuptools import find_packages, setup

setup(
    name='accent_plugind_client',
    version='0.2',
    description='a simple client library for the accent-plugind HTTP interface',
    author='Accent Authors',
    author_email='help@accentservices.com',
    url='http://accentvoice.io',
    packages=find_packages(),
    entry_points={
        'accent_plugind_client.commands': [
            'config = accent_plugind_client.commands:ConfigCommand',
            'market = accent_plugind_client.commands:MarketCommand',
            'plugins = accent_plugind_client.commands:PluginCommand',
            'status = accent_plugind_client.commands:StatusCheckerCommand',
        ],
    },
)
