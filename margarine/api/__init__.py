# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""Main API application for Margarine.

Models:

  * User
  
    * uuid4
    * username
    * email
    * name
    * password → md5(username:realm:password)
    
  * Bookmark (never deleted) (just spider?)

    * uuid5(url)
    * url
    * text → sync to object store
    * tags
    * notations

      * location
      * note

    * votes
    * subscribers
     
      * uuid4
      * subscribed_at

    * created_at
    * original_etag
    * parsed_at

Simply normalize the above to get back to aggregate agnostic representations.
  
"""

import logging

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

from flask import Flask

import margarine.logging

from margarine.parameters import Parameters

from margarine.api import information
from margarine.api.user import USER
from margarine.api.article import ARTICLE
from margarine.api.tag import TAG

logger = logging.getLogger(__name__)

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

APPLICATION = Flask(__name__)

APPLICATION.register_blueprint(USER, prefix = "{i.API_VERSION}/users".format(i = information))
APPLICATION.register_blueprint(ARTICLE, prefix = "{i.API_VERSION}/articles".format(i = information))
APPLICATION.register_blueprint(TAG, prefix = "{i.API_VERSION}/tags".format(i = information))

def _extract_flask_parameters(parameters):
    """Extract the flask parameters from Parameters.

    This is only necessary to use if translating the stored parameters in a
    Parameters object to parameters to flask.  This does not need to be used
    otherwise and is used internally to start the flask service as part of this
    module.

    """

    flask_parameters = {}

    if "host" in parameters:
        flask_parameters["host"] = parameters["host"]

    if "port" in parameters:
        flask_parameters["port"] = parameters["port"]
    
    if "debug" in parameters:
        flask_parameters["debug"] = parameters["debug"]

    return flask_parameters

if __name__ == "__main__":
    parameters = Parameters()
    parameters.parse()

    APPLICATION.run(**extract_flask_parameters(parameters))

