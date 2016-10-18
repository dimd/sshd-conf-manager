Description
===========

Utilities to subscribe to a redis section, be notified upon changes and do 
something with those changes. Currently, upon change notification, configuration
file update and process management is available. The project is well suited for
sshd management. Meaning, update of the sshd_config file and notification of
the sshd process running under supervisord_.

.. _supervisord: http://supervisord.org/

The project is written in python2

Installation
============
Use pip

.. code-block:: Bash

 pip install git+https://gitlabe1.ext.net.nokia.com/utas-security/sshd-conf-manager.git#egg=sshd_conf_manager

or if you have the repository checked out:

.. code-block:: Bash

 pip install sshd_conf_manager

Hopefully the project will be uploaded to a PyPi server soon. When this is done you will be able to:

.. code-block:: Bash

 pip install sshd_conf_manager

Usage
=====

The package includes an executable named ``sshd-conf-manager``.

Run ``sshd-conf-manager --help`` for a help text and usage info.

Once you run it, it will block and wait for redis notifications. When a change occurs in redis the 
sshd data are received and applied into the sshd_config file. Lastly, a HUP signal is sent to the sshd
process to reread the updated configuration.

Tests
=====

Tests can be run using tox or py.test. The tox method is recommended.

To install tox just do:

.. code-block:: Bash
 
 pip install tox

Then you'll be able to run the tests by running:

.. code-block:: Bash

 tox
