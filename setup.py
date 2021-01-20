#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='save-scummer',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'appdirs',
        'Click>=7.0',
        'python-dateutil',
        'pytimeparse',
        'pyyaml>=5.0',
        'tabulate',
    ],
    entry_points={
        'console_scripts': ['save-scummer=save_scummer.cli:ssc', 'ssc=save_scummer.cli:ssc'],
    },
)
