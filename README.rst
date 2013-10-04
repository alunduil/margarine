.. image:: https://secure.travis-ci.org/raxsavvy/margarine.png?branch=master
   :target: http://travis-ci.org/raxsavvy/margarine
   
Introduction
============

I can't believe it's not butter…margarine aims to be a zen (butter) web
browsing experience.  This tool adds features to an amalgamation of delicious,
the social bookmarking application, and readability, the excellent web article
renderer.

Motivations
===========

This project was created as a demo application for training purposes on cloud
application design.  It is not intended (but no one will be stopped) as a
replacement for delicious and readability.

Scope
=====

The following features are the large scale goals of margarine:

* Social Bookmarking
* Tagged Bookmarks
* Re-rendering of Bookmarks
* URL Shortening of Bookmarks
* Margin Notations on Bookmarks

Not all of these scope goals will be available in what will be marked a first
release.

Installation
============

The installer simply installs all the pieces with the current build system but
future work shall include splitting these up into separate bundles.  Due to the
single installer, installation is very easy:

:source: ``python setup.py install``
:pip:    ``pip install margarine``

Deployment
==========

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

Development
===========

You can use Vagrant to create a development environment locally with Chef & VirtualBox.
Be sure to set the proper attributes for your development environment in the chef.json 
sections in the Vagrantfile. More information is available `here <https://github.com/raxsavvy/margarine-chef>`.

Development follows a standard branching and forking model that most github
projects utilize.  Various components (tools) of the development process are
listed below.

:issues: Utilize github's issue system
:wiki:   Utilize github's wiki system
:features: Utilize `Margarine's Trello Board <https://trello.com/b/kYylJGe9/margarine>`_

