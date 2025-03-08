#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='accent-purge-db-sample-plugin',
    version='1.1',
    description='ACCENT sample plugin for archive before database clean',
    author='Accent',
    author_email='help@accentservices.com',
    url='https://github.com/accentcommunications/accent-purge-db',
    license='GPLv3',
    packages=find_packages(),
    entry_points={
        'accent_purge_db.archives': ['sample = accent_purge_db_sample.sample:archive_plugin'],
        'accent_purge_db.purgers': ['sample = accent_purge_db_sample.sample:PurgePlugin'],
    },
)
