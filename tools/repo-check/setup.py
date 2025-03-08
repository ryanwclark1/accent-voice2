import fnmatch
import os
from distutils.core import setup


def is_package(path):
    is_svn_dir = fnmatch.fnmatch(path, '*/.svn*')
    is_test_module = fnmatch.fnmatch(path, '*tests')
    return not (is_svn_dir or is_test_module)


packages = [p for p, _, _ in os.walk('repo_check') if is_package(p)]


setup(
    name='repo-check',
    version='1.0',
    description='Accent Merge assistant',
    author='Accent',
    author_email='ryanwclark@accentservices.com',
    url='https://github.com/accentcommunications/accent-tools',
    packages=packages,
    scripts=['bin/check_local_accent_repositories', 'bin/check_unmerged_branches'],
    license='GPLv3',
    long_description=open('README.md').read(),
)
