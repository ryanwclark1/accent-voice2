#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='accent-dird-broken-plugins',
    version='1.0',
    description='Accent Directory Daemon broken plugins',
    author='Accent Communications',
    author_email='dev+pkg@accentvoice.io',
    url='https://github.com/accentcommunications/accent-dird',
    packages=find_packages(),
    entry_points={
        'accent_dird.backends': [
            'broken = accent_dird_broken_plugins.broken_backend:BrokenPlugin',
            'broken_lookup = accent_dird_broken_plugins.broken_backend:BrokenLookup',
            'chained_broken_first_lookup = accent_dird_broken_plugins.broken_backend:ChainedBrokenFirstLookup',
            'chained_second_lookup = accent_dird_broken_plugins.broken_backend:ChainedSecondLookup',
        ],
        'accent_dird.services': [
            'broken_bus = accent_dird_broken_plugins.broken_service:BrokenBusPlugin',
        ],
    },
)
