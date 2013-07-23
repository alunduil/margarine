# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import redis
import logging

from margarine.parameters import Parameters
from margarine.helpers import URI

logger = logging.getLogger(__name__)

Parameters("keystore", parameters = [
    { # --tokens-url=TOKENS_URL; TOKENS_URL ← "redis://localhost"
        "options": [ "--url" ],
        "metavar": "TOKENS_URL",
        "default": "redis://localhost",
        "help": "The token storage system to use; defaults: %(default)s.",
        },
    ])

KEYSTORE_CONNECTIONS = {}

def get_keyspace(keyspace):
    """Using the keystore.url parameter we get a hash for storing data.

    If a connection has already been established we'll re-use that connection;
    otherwise, we'll create the connection and return the requested hash.

    .. note::
        Currently we only work with a Redis keystore using the redis-py binding
        layer.  If we decide to use other keystores (or even native python
        dicts) we'll ahve to re-evaluate this architecture.

    Returns
    -------

    An interface to the particular key collection requested.

    """

    global KEYSTORE_CONNECTIONS

    url = Parameters()["keystore.url"]

    uri = URI(url)

    if uri.path is not None:
        logger.warn("Redis database is specified in the keystore.url!")

    if keyspace not in KEYSTORE_CONNECTIONS:
        # Redis doesn't believe in named databases so we need to implement them:

        databases = {
                "tokens": 0,
                "verifications": 1,
                }

        logger.debug("port: %s", uri.port)
        logger.debug("type(port): %s", type(uri.port))

        port = 6379
        if uri.port is not None:
            port = int(uri.port)
            
        KEYSTORE_CONNECTIONS[keyspace] = redis.Redis(host = uri.host, port = port, db = databases[keyspace])

    return KEYSTORE_CONNECTIONS[keyspace]
    
