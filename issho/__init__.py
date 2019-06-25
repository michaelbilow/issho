# -*- coding: utf-8 -*-
"""Top-level package for issho."""

__author__ = """Michael Bilow"""
__email__ = "michael.k.bilow@gmail.com"
__version__ = "0.5.0"
__docformat__ = "restructuredtext"


from issho.issho import Issho

# module level doc-string
__doc__ = """
issho - simple connections to remote machines
=====================================================================
**issho** is a Python package providing a simple wrapper over
paramiko, providing = operators interacting with remote machines 

Main Features
-------------
Here are a few of the things that issho (should) do well:
  - execute commands on a remote box
  - transfer files to and from a remote easily
  - set up an SSH tunnel through a remote
  - run Hive & Spark jobs

TODOs
---------
  - make it easy to interact with hadoop
  - make it easy to configure new services
  - make it easy to add plugins to issho
"""
