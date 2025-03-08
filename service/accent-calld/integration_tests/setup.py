#!/usr/bin/env python3
# Copyright 2023 Accent Communications

from setuptools import setup

setup(
    name='accent_calld_test_helpers',
    version='1.0.0',
    description='Accent calld test helpers',
    author='Accent Authors',
    author_email='help@accentvoice.io',
    packages=['accent_calld_test_helpers'],
    package_dir={
        'accent_calld_test_helpers': 'suite/helpers',
    },
)
