# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import pymongo
import logging
import os
import pyrax

from margarine.parameters import Parameters
from margarine.parameters import CONFIGURATION_DIRECTORY
from margarine.helpers import URI

logger = logging.getLogger(__name__)

Parameters("datastore", parameters = [
    { # --datastore-url=URL; URL ← mongodb://localhost/test
        "options": [ "--url" ],
        "default": "mongodb://localhost/test",
        "help": \
                "The URL endpoint of the data store mechanism.  This can be " \
                "a local sqlite database but typically will be set to a " \
                "MongoDB instance.",
        }
    ])

DATASTORE_CONNECTION = None

def get_collection(collection):
    """Using the datastore.url parameter we get a collection for storing data.

    If a connection has already been established we'll re-use that connection;
    otherwise, we'll create the connection and return the requested collection.

    .. note::
        Currently we only work with a Mongo datastore using the pymongo binding
        layer.  If we decide to use other datastores we'll have to re-evaluate
        this architecture.

    Parameters
    ----------

    :collection: The MongoDB collection to return after connecting.

    Returns
    -------

    A collection for datastore interaction.

    """

    global DATASTORE_CONNECTION

    url = Parameters()["datastore.url"]

    uri = URI(url)

    logger.debug("url: %s", url)
    logger.debug("uri: %s", uri)

    if DATASTORE_CONNECTION is None:
        DATASTORE_CONNECTION = pymongo.MongoClient(url)

    database_name = uri.path

    logger.debug("database_name: %s", database_name)

    if "/" in database_name:
        database_name = database_name.replace("/", "", 1).replace("/", "_")

    database = DATASTORE_CONNECTION[database_name]

    indexes = {
            "users": [
                [
                    [ ( "username", pymongo.ASCENDING ), ],
                    { 
                        "unique": True,
                        "drop_dups": True,
                        "background": True,
                        },
                    ],
                ],
            }

    logger.debug("collection: %s", collection)

    for index in indexes.get(collection, []):
        logger.debug("index: %s", index)
        logger.debug("index-args: %s", index[0])
        logger.debug("index-kwargs: %s", index[1])

        database[collection].ensure_index(index[0], **index[1])

    return database[collection]

Parameters("pyrax", parameters = [
    { # --pyrax-configuration=FILE; FILE ← CONFIGURATION_DIRECTORY/pyrax.ini
        "options": [ "--configuration" ],
        "default": os.path.join(CONFIGURATION_DIRECTORY, "pyrax.ini"),
        "help": \
                "The configuration file containing the pyrax credentials " \
                "used by %(prog)s.  Default: %(default)s.",
        },
    ])

def get_container(container):
    """Using the pyrax interface retrieve a container object for storing data.

    Reconnects for every container provided.  

    .. note::
        This needs to be checked for correctness.  This needs to be checked
        that the container does indeed hold open the connection and that the
        connection is closed properly when the container goes out of scope.

    Parameters
    ----------

    :container: The name of the container to return for interaction.

    Returns
    -------

    A container for datastore interaction.

    """

    pyrax.set_credential_file(Parameters()["pyrax.configuration"])

    return pyrax.cloudfiles.create_container(container)

