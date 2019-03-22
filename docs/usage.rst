=====
Usage
=====

First, set up ``issho`` by following the instructions in
setup_.

To use ``issho`` in a project::

    from issho import Issho


Basic Commands
--------------

The first thing to do::

    devbox = Issho('dev')

This will set up a connection to the machine referred to as ``dev`` in your
``.ssh/config``.

To run a command on your devbox, you can do the following::

    devbox.exec('echo "Hello, world!"')
    'Hello, world!'

Note that the data is printed, not returned.

You can copy a file to or from your remote using ``put`` & ``get``::

    output_filename = 'test.txt'
    copy_back_filename = 'get_test.txt'
    with open(output_file, 'w') as f:
        f.write('\n'.join(map(str, range(5))))
    devbox.put(output_filename)
    devbox.exec('cat {}'.format(output_filename))
    devbox.get(output_file, copy_back_filename)
    for line in open(copy_back_filename):
        print(line.strip())

Convenience Functions
---------------------

``issho`` offers several convenience functions, including this for Hive::

    devbox.hive('select * from burgers limit 10;')
    devbox.hive('burger_query.sql')


.. _setup: ./setup.html
