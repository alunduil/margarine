# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""Frontend for Margarine.

This frontend flask application handles gluing the HTML provided to a browser
to the API (blend).  Ideally, this will be completely migrated to cloudfiles
and completely served by CDN but the following challenges potentially damper
that plan:

* A URL in cloudfiles is a key to a particular resource.  If we want to have
  a *dynamic* website that knows how to handle URLs that look like
  /articles/<uuid> we need a mechanism to have a generic router (which won't
  happen).  Potentially, this could be solved with query parameters in the URL
  but it's not clear if cloudfiles appropriately ignores query parameters for
  this solution to work.

  Otherwise, if we can map non-unique keys to a single resources javascript
  does contain functionality that allows us to interpret the URL and perform
  the appropriate dynamic programming.

.. note::
    Simple testing with CloudFiles public URLs did show that retrieval of the
    same resource happened if a query string was appended to the URL.  Once,
    we have an acceptable interface we can decompose it to just the raw HTML
    (with javascript being the binding) for a truly scalable SOA application.

"""

import logging
import socket

from flask import Flask
from flask import render_template

from margarine.parameters import Parameters
from margarine.parameters import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

# Duplicate definition of flask parameters

Parameters("flask", parameters = [
    { # --flask-host=HOST; HOST ← "127.0.0.1"
        "options": [ "--host" ],
        "default": "127.0.0.1",
        "help": "The IP to bind the API daemon; default: %(default)s.",
        },
    { # --flask-port=PORT; PORT ← "5000"
        "options": [ "--port" ],
        "type": int,
        "default": 5000,
        "help": "The port to bind the API daemon; default: %(default)s.",
        },
    { # --flask-debug
        "options": [ "--debug" ],
        "action": "store_true",
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

TINGE = Flask(__name__)

# TODO Anything else required for the frontend?

@TINGE.route('/')
def home_page():
    """Return a simple homepage outlining Margarine and allowing signups.

    This is split into two sides:

    * Login and sign-up form on the left
    * Small about and small list of recently added article subjects

    """

    return render_template('index.html')

Parameters("api", parameters = [
    { # --api-endpoint=URL; URL ← http://HOSTNAME:5050
        "options": [ "--endpoint" ],
        "default": "http://" + socket.gethostname() + ":5050",
        "help": \
                "The API endpoint or rather the URL endpoint for the blend " \
                "processes.  Defaults to %(default)s",
        },
    ])

@TINGE.route('/article')
def view_article():
    """Return the sanitized view of the article with interface elements.

    The interface elements are a sidebar including the following functions:

    * article star (subscribe)
    * tag cloud (add tags)
    * profile interaction

    If the user isn't logged in they'll see a login form instead of profile
    interaction and will have a grayed out unusable star.

    .. note::
        Should tags be only addable by authenticated users?

    A search box should be shown in the sidebar as well.

    Perhaps the following layout:

    +--------+----------+
    | SEARCH | STAR     |
    +--------+----------+
    | TAG CLOUD         |
    +-------------------+
    | Sign In | Sign Up |
    +-------------------+

    .. note::
        Should the URL schema change to reflect a scheme that will work with
        the pure static page layout (i.e. /article?id=UUID5)?

    Expectations
    ------------

    A query parameter, ``_id``, will be passed with the UUID5 of the article
    to be viewed.

    """

    return render_template('article.html', api_endpoint = Parameters()["api.endpoint"])

logger.debug("error_handlers: %s", TINGE.error_handler_spec)

# TODO Find out why this might be necessary.
#TINGE.config["SERVER_NAME"] = Parameters()["server.name"]

logger.debug("url map: %s", TINGE.url_map)

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
    TINGE.run(**_extract_flask_parameters(Parameters().parse()))

