#!/usr/bin/env python3
# Copyright 2023 Accent Communications

from setuptools import setup

setup(
    name='accent_confd_test_helpers',
    version='1.0.0',
    description='Accent confd test helpers',
    author='Accent Authors',
    author_email='help@accentvoice.io',
    packages=['accent_confd_test_helpers', 'accent_confd_test_helpers.helpers'],
    package_dir={
        'accent_confd_test_helpers': 'suite/helpers',
        'accent_confd_test_helpers.helpers': 'suite/helpers/helpers',
    },
)
