=======
History
=======

0.3.1 (2019-04-11)
------------------
* Fix bug regarding ssh vs local user identity

0.3.0 (2019-04-09)
------------------
* Add more configuration and reduce variables on the ``Issho`` object.
* Allow ``prompt_toolkit>=1.0.10`` to allow ``jupyter`` interoperability.
* Set up useful passwords using ``issho config``

0.2.5 (2019-03-25)
------------------
* Clean up hive operator and sftp callback
* Note that ``issho`` is incompatible with ``jupyter_console<6.0`` and ``ipython<7.0``


0.2.4 (2019-03-25)
------------------
* Fix bug in hive operator

0.2.3 (2019-03-25)
------------------
* Add ``.readthedocs.yml``; docs build now passes.

0.2.2 (2019-03-24)
------------------
* Clean up docs, try to have a passing build

0.2.1 (2019-03-22)
------------------
* Add docstrings for all functions
* Add autodocs
* Switch out ``bumpversion`` for ``bump2version``

0.2.0 (2019-03-22)
------------------
* Add Hive function
* Add configuration CLI
* Fix Travis config to Python 3.5+

0.1.0 (2019-02-26)
------------------

* First release on PyPI.
