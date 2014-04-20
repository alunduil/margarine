# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import bs4
import datetime
import Crypto.Hash.SHA256
import logging
import tornado.httpclient

from margarine import datastores
from margarine import queues
from margarine.spread import CONSUMERS

logger = logging.getLogger(__name__)


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

        article['body'] = datastores.get_gridfs().put(soup.get_text(), encoding = 'utf-8')

        logger.debug('article[body]: %r', article['body'])

        article['parsed_at'] = datetime.datetime.now()
        article['updated_at'] = datetime.datetime.now()

        article.pop('etag', None)  # Don't include etag in etag calculation.

        article['etag'] = Crypto.Hash.SHA256.new(''.join(sorted([ str(_) for _ in article.values() ]))).hexdigest()
        logger.debug('etag: %s', article['etag'])

        logger.debug('article: %s', article)

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
