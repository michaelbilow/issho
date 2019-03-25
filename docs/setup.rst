=====
Setup
=====

After installing ``issho``, you will want to do some setup.

First, add the machine you want a profile for to your
``.ssh/config``. For example, if you want to add a machine
with the alias ``dev`` (the default for ``issho``),
you would add the following lines to your ssh config.

.. code-block:: console

    Host dev
        HostName your-host-name.com
        Port XXXXX
        User your_user

Once this is set up, you can set up passwords
and common variables using the following command:

.. code-block:: console

    issho config dev

This command will drop you into an interactive prompt where
you can enter passwords and configuration variables.
