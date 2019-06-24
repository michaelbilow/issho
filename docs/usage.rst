=====
Usage
=====

Configuration
-------------

After installation, set up ``issho`` by following the instructions in
setup_.


Basic Commands
--------------

To use ``issho`` in a project::

    from issho import Issho

The first thing to do::

    devbox = Issho('dev')

This will set up a connection to the machine referred to as ``dev`` in your
``.ssh/config``. Note that this will **only** work if Issho has already been
configured_.

To run a command on your devbox, you can do the following::

    devbox.exec('echo "Hello, world!"')
    'Hello, world!'

Note that the data is printed, not returned.

You can copy a file to or from your remote using ``put`` & ``get``::

    output_filename = 'test.txt'
    copy_back_filename = 'get_test.txt'
    with open(output_filename, 'w') as f:
        f.write('\n'.join(map(str, range(5))))
    devbox.put(output_filename)
    devbox.exec('cat {}'.format(output_filename))
    devbox.get(output_filname, copy_back_filename)
    for line in open(copy_back_filename):
        print(line.strip())

Convenience Functions
---------------------

Shell Commands
==============

Instead of using ``devbox.exec(cmd, *args)``, you can write ``devbox.cmd(*args)``::

    devbox.touch('my_test.txt')
    devbox.ls(' | grep my_test.txt')
    devbox.rm('my_test.txt')

Underscores in the function name are converted to spaces::

    devbox.seq_5()

Hadoop & HDFS
=============

Hadoop functions can be accessed using the ``.hadoop`` or ``.hdfs`` methods.
You do not need to prepend the dash to hadoop operations, though they will
still work with it::

    devbox.hdfs('ls /tmp | grep test')
    devbox.hadoop('mkdir -p /tmp/test/')


``put`` and ``get`` can also get from HDFS, if passed a qualified
HDFS path, or if the `hadoop` option is passed.::

    devbox.put('test.txt', '/tmp/my_folder/', hadoop=True)
    devbox.get('hdfs:///tmp/myfile')

Hive
====

``issho`` offers several convenience functions, including this for Hive::

    devbox.hive('select * from burgers limit 10;')
    devbox.hive('burger_query.sql')

Results from hive queries can be output locally by passing an output_filename::

    devbox.hive('select stack(3, "hello", "cruel", "world") as val;', "hello.tsv")

Spark
=====

``issho`` can trigger a spark job using ``spark-submit``; you can call it using
```spark_submit`` or ``spark``::

    devbox.spark(application='test.jar', application_class='com.test.SparkWorkflow'...)



.. _setup: ./setup.html
.. _configured: ./setup.html
