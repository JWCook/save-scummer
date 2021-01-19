#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='save-scummer',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['appdirs', 'Click>=7.0', 'pyyaml>=5.0'],
    entry_points={
        'console_scripts': ['ssc=save_scummer.main:ssc'],
    },
)
