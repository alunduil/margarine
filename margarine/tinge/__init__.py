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

"""

import logging

from flask import Flask

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

# TODO Add tinge methods.

logger.debug("error_handlers: %s", TINGE.error_handler_spec)

TINGE.config["SERVER_NAME"] = Parameters()["server.name"]

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

    if "host" in parameters:
        flask_parameters["host"] = parameters["host"]

    if "port" in parameters:
        flask_parameters["port"] = parameters["port"]
    
    if "debug" in parameters:
        flask_parameters["debug"] = parameters["debug"]

    return flask_parameters

def main():
    TINGE.run(**_extract_flask_parameters(Parameters().parse()))

