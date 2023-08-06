#!/usr/bin/env python
import os
import sys

if sys.version_info < (3, 8):
    print('Error: dbt does not support this version of Python.')
    print('Please upgrade to Python 3.8 or higher.')
    sys.exit(1)

try:
    from setuptools import find_namespace_packages
except ImportError:
    # the user has a downlevel version of setuptools.
    print('Error: dbt requires setuptools v40.1.0 or higher.')
    print('Please upgrade setuptools with "pip install --upgrade setuptools" '
          'and try again')
    sys.exit(1)

from pathlib import Path
from setuptools import setup


# pull the long description from the README
README = Path(__file__).parent / "README.md"


# used for this adapter's version and in determining the compatible dbt-core version
VERSION = Path(__file__).parent / "dbt/adapters/cratedb/__version__.py"


def _plugin_version() -> str:
    """
    Pull the package version from the main package version file
    """
    attributes = {}
    exec(VERSION.read_text(), attributes)
    return attributes["version"]


package_name = "dbt-cratedb"
package_version = "1.5.2"
description = """The crate adapter plugin for dbt (data build tool)"""
dbt_version = '1.5.2'

CRATE_DRIVER_VERSION = '0.32.0'

setup(
    name=package_name,
    version=_plugin_version(),
    description=description,
    long_description=README.read_text(),
    long_description_content_type='text/markdown',
    author="Smartnow",
    author_email="julio@smartnow.la",
    url="",
    packages=find_namespace_packages(include=['dbt', 'dbt.*']),
    package_data={
        'dbt': [
            'include/cratedb/dbt_project.yml',
            'include/cratedb/sample_profiles.yml',
            'include/cratedb/macros/*.sql',
            'include/cratedb/macros/**/*.sql',
        ]
    },
    install_requires=[
        'dbt-core=={}'.format(dbt_version),
        'crate=={}'.format(CRATE_DRIVER_VERSION),
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8.2",
)
