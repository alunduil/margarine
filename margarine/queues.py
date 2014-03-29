# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import kombu
import logging

import margarine.parameters.queue  # flake8: noqa

from margarine.parameters import PARAMETERS

logger = logging.getLogger(__name__)

ARTICLES_TOPIC_EXCHANGE = kombu.Exchange('articles.topic', type = 'topic', delivery_mode = 'transient')

ARTICLES_CREATE_QUEUE = kombu.Queue('articles.create', ARTICLES_TOPIC_EXCHANGE, routing_key = 'articles.create')

ARTICLES_FANOUT_EXCHANGE = kombu.Exchange('articles.fanout', type = 'fanout', delivery_mode = 'transient')

QUEUE_CONNECTION = None


def get_connection():
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
