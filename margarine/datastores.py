# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import gridfs
import logging
import pymongo

import margarine.parameters.datastores  # flake8: noqa

from margarine.parameters import PARAMETERS
from margarine.helpers import URI

logger = logging.getLogger(__name__)

DATASTORE_DATABASE = None


def get_collection(collection_name):
    '''Retrieve a collection from the configured MongoDB URI.

    This will create a new connection if required and retrieve the named
    collection.

    Parameters
    ----------

    :``collection_name``: MongoDB collection to retrieve

    Return
    ------

    MongoDB collection requested.

    '''

    return get_database()[collection_name]


def get_database():
    '''Retrieve the database from the configured MongoDB URI.

    This will create a new connection if required and retrieve the database.

    Return
    ------

    MongoDB database configured.

    '''

    global DATASTORE_DATABASE

    if DATASTORE_DATABASE is not None:
        return DATASTORE_DATABASE

    logger.info('STARTING: get database')

    mongo_url = PARAMETERS['datastore.url']

    connection = pymongo.MongoClient(url)

    database_name = URI(mongo_url).path
    logger.debug('database_name: %s', database_name)

    if database_name.startswith('/'):
        database_name = database_name[1:]

    DATASTORE_DATABASE = connection[database_name]

    logger.info('STOPPING: get database')

    return DATASTORE_DATABASE


def get_gridfs():
    '''Retrieve the GridFS from the configured MongoDB URI.

    This will create a new connection if required and retrieve the database's
    GridFS.

    Return
    ------

    MongoDB GridFS.

    '''

    return gridfs.GridFS(get_database())
