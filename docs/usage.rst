=====
Usage
=====

First, set up ``issho`` by following the instructions in
setup_.

To use ``issho`` in a project::

    from issho import Issho


Working with a devbox
---------------------

The first thing to do::

    devbox = Issho('dev')

This will set up a connection to the machine referred to as ``dev`` in your
``.ssh/config``.



.. _setup: ./setup.html
