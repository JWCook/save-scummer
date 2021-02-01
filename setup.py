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
        'click-completion',
        'halo',
        'python-dateutil',
        'pytimeparse',
        'pyyaml>=5.0',
        'tabulate',
        'watchdog',
    ],
    extras_require={
        'dev': ['black', 'isort', 'flake8', 'mypy', 'pre-commit', 'pytest', 'pytest-cov'],
        'build': ['coveralls', 'twine', 'wheel'],
    },
    entry_points={
        'console_scripts': ['save-scummer=save_scummer.cli:ssc', 'ssc=save_scummer.cli:ssc'],
    },
)
