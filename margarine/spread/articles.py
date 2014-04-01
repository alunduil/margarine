# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import bs4
import Crypto.Hash.SHA256
import datetime
import kombu
import logging
import tornado

from margarine import queues
from margarine import datastores
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
        producer.publish(
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


def sanitize_article(body, message):
    '''Sanitize and store the given article's HTML.

    Strips down the bulky HTML for the article and stores the simplified
    version in GridFS.

    Parameters
    ----------

    :``UUID``: UUID of the article

    '''

    logger.info('STARTING: sanitize HTML: %s', body['uuid'])

    article = datastores.get_collection('articles').find_one({ '_id': body['uuid'].hex })

    client = tornado.httpclient.HTTPClient()

    response = client.fetch(article['original_url'], method = 'HEAD')

    original_etag = response.headers['ETag']
    logger.debug('ETag: %s', original_etag)

    if article.get('original_etag') == original_etag:
        logger.info('STOPPING: sanitize HTML: %s—not modified', body['uuid'])
    else:
        article['original_etag'] = original_etag

        response = client.fetch(article['original_url'])
        soup = bs4.BeautifulSoup(response.buffer)

        if 'body' in article:
            article.setdefault('previous_bodies', []).append(article['body'])

        article['body'] = datastores.get_gridfs().put(soup.get_text())

        article['parsed_at'] = datetime.datetime.now()
        article['updated_at'] = datetime.datetime.now()

        article.pop('etag', None)  # Don't include etag in etag calculation.

        article['etag'] = Crypto.Hash.SHA256.new(''.join(sorted([ str(_) for _ in article.values() ]))).hexdigest()
        logger.debug('etag: %s', article['etag'])

        _id = article.pop('_id')

        datastores.get_collection('articles').update({ '_id': _id }, { '$set': article }, upsert = True)

        logger.info('STOPPING: sanitize HTML: %s', body['uuid'])

    message.ack()


CONSUMERS.append(
    {
        'queues': [ queues.ARTICLES_SANITIZE_QUEUE ],
        'accept': [ 'pickle' ],
        'callbacks': [ sanitize_article ],
    }
)
