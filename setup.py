#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'sshtunnel>=0.1.4',
    'keyring>=18.0.0',
    'paramiko>=2.4.0',
    'cryptography==2.4.2',  # https://github.com/paramiko/paramiko/issues/1369
    'prompt_toolkit>=2.0.5',
    'toml>=0.10.0',
    'fire>=0.1.3'
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Michael Bilow",
    author_email='michael.k.bilow@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="issho allows easy access to simple commands on a remote machine.",
    entry_points='''
        [console_scripts]
        issho=issho.cli:main
    ''',
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='issho,paramiko,keyring,ssh,sftp,python,python-fire,prompt-toolkit,pysftp,sshed,sshtunnel',
    name='issho',
    packages=find_packages(include=['issho']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/michaelbilow/issho',
    version='0.2.3',
    zip_safe=False,
)
