# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import kombu
import logging

from margarine import datastores
from margarine import queues
from margarine.parameters import PARAMETERS
from margarine.spread import CONSUMERS

logger = logging.getLogger(__name__)


def create_article(body, message):
    '''Create the given article.

    Sets up the metadata for the given article and passes along the datastore
    ID to secondary tasks.

    Parameters
    ----------

    :``UUID``: UUID of the article.
    :``URL``:  URL of the article.

    '''

    logger.info('STARTING: create article: %s', body['url'])

    article = datastores.get_collection('articles').find_one({ '_id': body['uuid'].hex })

    if article is None:
        article = {}

    article.setdefault('_id', body['uuid'].hex)
    article.setdefault('created_at', datetime.datetime.now())
    article.setdefault('original_url', body['url'])
    article.setdefault('updated_at', datetime.datetime.now())

    logger.debug('article: %s', article)

    _id = article.pop('_id')
    datastores.get_collection('articles').update({ '_id': _id }, { '$set': article }, upsert = True)

    with kombu.pools.producers[queues.get_connection()].acquire(block = True) as producer:
        publish = queues.get_connection().ensure(producer, producer.publish, max_retries = PARAMETERS['queue.retries'])
        publish(
            { 'uuid': body['uuid'] },
            serializer = 'pickle',
            compression = 'bzip2',
            exchange = queues.ARTICLES_FANOUT_EXCHANGE,
            declare = [ queues.ARTICLES_FANOUT_EXCHANGE ],
            routing_key = 'articles.secondary'
        )

    logger.info('STOPPING: create article: %s', body['url'])

    message.ack()


CONSUMERS.append(
    {
        'queues': [ queues.ARTICLES_CREATE_QUEUE ],
        'accept': [ 'pickle' ],
        'callbacks': [ create_article ],
    }
)
