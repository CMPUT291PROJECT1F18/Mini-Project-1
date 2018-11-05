##############
mini-project-1
##############

.. image:: https://travis-ci.org/CMPUT291PROJECT1F18/Mini-Project-1.svg?branch=master
    :target: https://travis-ci.org/CMPUT291PROJECT1F18/Mini-Project-1
    :alt: Build Status

.. image:: https://readthedocs.org/projects/mini-project-1/badge/?version=latest
    :target: https://mini-project-1.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Requirements
============

* Python 3.6+


Overview
========

mini-project-1 is a simple command line interface (CLI) tool for interacting
with a database service that provide information similar to popular ride
sharing applications.


Installation
============

mini-project-1 can be installed from source by running:

.. code-block:: bash

    pip install .

Within the same directory as mini-project-1's ``setup.py`` file.


Usage
=====

After installing mini-project-1's shell can be started by the following console
command:

.. code-block:: bash

    mini-project-1 -i example.db -v


This will create an initial mini-project-1 database named ``example.db`` at
your current directory and will immediately give you a prompt to login to
such database.

To get additional usage help on starting mini-project-1 run the following
console command:

.. code-block:: bash

    mini-project-1 --help
