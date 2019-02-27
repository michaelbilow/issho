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
    'cryptography==2.4.2'  # https://github.com/paramiko/paramiko/issues/1369
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="issho allows easy access to simple commands on a remote machine.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='issho,paramiko,sshtunnel,keyring,ssh,sftp,pysftp,sshed,python',
    name='issho',
    packages=find_packages(include=['issho']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/michaelbilow/issho',
    version='0.1.0',
    zip_safe=False,
)
