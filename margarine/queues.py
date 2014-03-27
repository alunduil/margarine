# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import kombu
import logging

import margarine.parameters.queue  # flake8: noqa

from margarine.parameters import PARAMETERS

logger = logging.getLogger(__name__)

QUEUE_CONNECTION = None


def get_queue_connection():
    '''Retrive the queue connection from the configured queue URI.

    Creates a new connection if required.

    Return
    ------

    Connection to queue.

    '''

    global QUEUE_CONNECTION

    if QUEUE_CONNECTION is None:
        logger.info('STARTING: get queue connection')

        queue_url = PARAMETERS['queue.url']
        logger.debug('queue URL: %s', queue_url)

        QUEUE_CONNECTION = kombu.Connection(queue_url)

        logger.info('STOPPING: get queue connection')

    return QUEUE_CONNECTION
