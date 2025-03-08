#!/usr/bin/env python3
# Copyright 2023 Accent Communications

from setuptools import find_packages, setup

setup(
    name='accent-debug',
    version='1.1',
    author='Accent Authors',
    author_email='help@accentservices.com',
    url='http://accentvoice.io',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'accent-debug = accent_debug.main:main',
        ],
        'accent_debug.commands': [
            'access = accent_debug.access:AccessCommand',
            'capture = accent_debug.capture:CaptureCommand',
            'collect = accent_debug.collect:CollectCommand',
            'public-ip = accent_debug.public_ip:PublicIPCommand',
            'http-request-duration = accent_debug.http_request_duration:HTTPRequestDurationCommand',
        ],
    },
)
