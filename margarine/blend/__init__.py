# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""API for Margarine.

This API provides three resources with various actions (outlined more
completely in the appropriate module).  The resources are articles, users, and
tags.  The structure of these data types is shown below and have been optimized
in this form for a document store such as MongoDB.

Data Aggregates
===============

User
----

Fields
''''''

:_id:      Default MongoDB ID
:username: User's handle
:email:    User's email address
:name:     User's full name
:hash:     User's hash for HTTP Digest ← md5(username:realm:password)

Actions
'''''''

* Sign-Up (Create a User)
* Change Username (thus, username is not _id)
* Delete Account
* View Meta-information
* Login (Retrieve a token)

Article
-------

Fields
''''''

:_id:              UUID5 of the URL
:original:         Sub-document with original meta-information:

  :url:            Original article's URL
  :etag:           Original article's ETAG

:tags:             List of tags for this article
:notations:        List of notations (sub-documents):

  :location:       Where the notation is attached
  :note:           Text of the notation

:subscriber_count: Count of subscribers (article:user map is stored elsewhere)
:created_at:       Time of creation
:parsed_at:        Last time of parsing

:text:             Sanitized text of the article (stored in an object store)

.. note::
    The ``text`` field of an article is not stored in the same datastore
    (assuming a document store) but is stored in an object store such as riak,
    rackspace's cloud files, &c.  This choice is due to the 16MB document limit
    present in MongoDB and allows us to potentially serve this in alternative
    method and not worry about GridFS.

Actions
'''''''

* Submit URL (Create an Article)
* Subscribe (favorite, star, &c) to an article
* Tag an article
* View an article

Subscription
------------

A structure created to simplify storage of subscription information.  This
places subscriptions into an atomic unit of work without fear of hitting
MongoDB's 16MB document size limit.

This structure doesn't have any of its own actions as a result and simply helps
the other structures' actions.

Fields
''''''

:article_id: ID of the article for this subscription
:user_id:    ID of the user for this subscription
:created_at: Time of creation

.. note::
    The ``_id`` field is ignored and both ``article_id`` and ``user_id`` are
    indexed for sorting searches.

URL Summary
-----------

.. note::
    All URLs are assumed to be prefixed with the version string (i.e. /v1).

:``/users/<username>``:          GET,PUT,DELETE
:``/users/<username>/password``: GET,POST
:``/users/<username>/token``:    GET

"""

import logging
import socket

from flask import Flask
from flask import url_for

from margarine.parameters import Parameters
from margarine.parameters import configure_logging

configure_logging()

from margarine.blend import information

from margarine.blend.user import USER
from margarine.blend.user import UnauthorizedError
from margarine.blend.user import http_401_handler

from margarine.blend.article import ARTICLE
from margarine.blend.tag import TAG

logger = logging.getLogger(__name__)

Parameters("flask", parameters = [
    { # --flask-host=HOST; HOST ← "127.0.0.1"
        "options": [ "--host" ],
        "default": "127.0.0.1",
        "help": "The IP to bind the API daemon; default: %(default)s.",
        },
    { # --flask-port=PORT; PORT ← "5050"
        "options": [ "--port" ],
        "type": int,
        "default": 5050,
        "help": "The port to bind the API daemon; default: %(default)s.",
        },
    { # --flask-debug
        "options": [ "--debug" ],
        "action": "store_true",
        "type": bool,
        "default": False,
        "help": "Enable debugging of the flask application.",
        },
    ])

Parameters("server", parameters = [
    { # --server-name=NAME; NAME ← HOSTNAME
        "options": [ "--name" ],
        "default": socket.gethostname(),
        "help": \
                "The base name used in URL generation.  This defaults to the" \
                "host's FQDN.",
        },
    ])

BLEND = Flask(__name__)

def _prefix(name):
    """Return the prefix for the API endpoint name given.

    Parameters
    ----------

    :name: The name of the API prefix.

    Returns
    -------

    The true prefix for the API section given the prefix name.

    """

    return "/{i.API_VERSION}/{name}".format(i = information, name = name)

BLEND.register_blueprint(USER, url_prefix = _prefix("users"))
BLEND.register_blueprint(ARTICLE, url_prefix = _prefix("articles"))
BLEND.register_blueprint(TAG, url_prefix = _prefix("tags"))

logger.debug("user resource directory: %s", USER.root_path)
logger.debug("article resource directory: %s", ARTICLE.root_path)
logger.debug("tag resource directory: %s", TAG.root_path)

BLEND.error_handler_spec[None][401] = http_401_handler

logger.debug("error_handlers: %s", BLEND.error_handler_spec)

# TODO Find out why this might be necessary.
#BLEND.config["SERVER_NAME"] = Parameters()["server.name"]

logger.debug("url map: %s", BLEND.url_map)

def _extract_flask_parameters(parameters):
    """Extract the flask parameters from Parameters.

    This is only necessary to use if translating the stored parameters in a
    Parameters object to parameters to flask.  This does not need to be used
    otherwise and is used internally to start the flask service as part of this
    module.

    Parameters
    ----------

    :parameters: The Parameters object to extract flask parameters from.

    """

    flask_parameters = {}

    if "flask.host" in parameters:
        flask_parameters["host"] = parameters["flask.host"]

    if "flask.port" in parameters:
        flask_parameters["port"] = parameters["flask.port"]
    
    if "flask.debug" in parameters:
        flask_parameters["debug"] = parameters["flask.debug"]

    return flask_parameters

def main():
    BLEND.run(**_extract_flask_parameters(Parameters().parse()))

