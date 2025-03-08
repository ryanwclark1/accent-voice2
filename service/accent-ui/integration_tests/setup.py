#!/usr/bin/env python3
# Copyright 2023 Accent Communications

from setuptools import setup

setup(
    name='accent_ui_test_helpers',
    version='1.0.0',
    description='Accent UI test helpers',
    author='Accent Authors',
    author_email='help@accentvoice.io',
    packages=['accent_ui_test_helpers', 'accent_ui_test_helpers.pages'],
    package_dir={
        'accent_ui_test_helpers': 'suite/helpers',
        'accent_ui_test_helpers.pages': 'suite/helpers/pages',
    },
)
