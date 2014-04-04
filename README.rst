Description
===========

It's not butter…margarine aims to be a zen (butter) web browsing experience.
This tool adds features to an amalgamation of delicious, the social bookmarking
application, and readability, the excellent web article renderer.

This project was created as a demo application for training purposes on cloud
application design.  It is not intended (but no one will be stopped) as a
replacement for delicious and readability.

Installation
============

This package is stored in PyPI and can be installed the standard way::

    pip install margarine

The latest release available is:

.. image:: https://badge.fury.io/py/margarine.png
    :target: http://badge.fury.io/py/margarine

If you would prefer to clone this package directly from git or assist with
development, the URL is https://github.com/raxsavvy/margarine and the current
status of the build is:

.. image:: https://secure.travis-ci.org/raxsavvy/margarine.png?branch=master
   :target: http://travis-ci.org/raxsavvy/margarine

Usage
=====

Margarine has several coordinating applications that get installed and need to
be running in order to provide all of the intended functionality:

:blend:  The API daemon that provides the web service with the application
         logic and connects the frontend to the backend processors.
:tinge:  The frontend for margarine that provides the web browseable interface
         to the application.
:spread: The backend daemon process that does non-interactive processing.

The ``tinge`` and ``blend`` processes can be deployed as a WSGI service if
desired (it is written with flask) but also has a built in web service that
can be used for small or development deployments.

The ``spread`` daemon is designed to work with ``start-stop-daemon`` to run in
the background on a server.  The ``spread`` daemon listens to a configurable
message queue but can be configured to talk directly with the ``blend``
process.

A fully functional environment can be spun up by using `vagrant`_:

    vagrant up

Authors
=======

* Alex Brandt <alunduil@alunduil.com>
* Hart Hoover <hart.hoover@gmail.com>
* Wayne Walls <wayneawalls@gmail.com>

Known Issues
============

Known issues can be found in the github issue list at
https://github.com/raxsavvy/margarine/issues.

.. _vagrant: http://www.vagrantup.com/
