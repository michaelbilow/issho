======
issho
======

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/michaelbilow/issho/master/LICENSE
    :alt: License

.. image:: https://img.shields.io/travis/michaelbilow/issho.svg
    :target: https://travis-ci.org/michaelbilow/issho

.. image:: https://readthedocs.org/projects/issho/badge/?version=latest
    :target: https://issho.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/issho.svg
    :target: https://pypi.python.org/pypi/issho

.. image:: https://img.shields.io/conda/vn/conda-forge/issho.svg
    :target: https://anaconda.org/conda-forge/issho
    :alt: Conda Version

.. image:: https://img.shields.io/conda/pn/conda-forge/issho.svg
    :target: https://anaconda.org/conda-forge/issho
    :alt: Conda Platforms

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: Code style: black

.. image:: https://pepy.tech/badge/issho
    :target: https://pepy.tech/project/issho
    :alt: Downloads

``issho`` and intuitive wrapper over paramiko_ for configuring
and talking to a remote host. keyring_ is used to
manage secrets locally.

``issho`` is designed such that interacting with a
single, heavily used remote machine should
be *easy*, and working with more than one remote
machine should be *simple*.


* Free software: MIT license
* Documentation: https://issho.readthedocs.io.

Installation
------------

Install with ``pip`` or ``conda``

::

    pip install issho


::

    conda install -c conda-forge issho


Features
--------

* Simple access to simple commands
    - Port forwarding
    - Executing commands over ssh
    - Transferring files over sftp
    - Running a hive query

Credits
-------

This package was created with Cookiecutter_
and the `audreyr/cookiecutter-pypackage`_ project template.

The sftp work and (future)testing framework is adapted from `Jeff Hinrichs`_'s
excellent pysftp_ package, and some of the ssh
framework is inspired by `Colin Wood`_'s sshed_.

Shout out to `Spencer Tipping`_, `Neal Fultz`_, and `Factual`_
for helping me learn to write my own tools.

Thanks to `Michael Vertuli`_ for helping test.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _paramiko: http://www.paramiko.org/
.. _sshed: https://github.com/cwood/sshed
.. _pysftp: https://bitbucket.org/dundeemt/pysftp
.. _keyring: https://github.com/jaraco/keyring
.. _Jeff Hinrichs: https://bitbucket.org/dundeemt/
.. _Colin Wood: https://github.com/cwood
.. _Spencer Tipping: https://github.com/spencertipping
.. _Neal Fultz: https://github.com/nfultz
.. _Michael Vertuli: https://github.com/vertuli
.. _Factual: https://www.factual.com
