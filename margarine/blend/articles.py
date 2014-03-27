# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import json
import kombu
import kombu.pools
import logging
import pytz
import re
import socket
import tornado.web
import uuid

import margarine.parameters.tinge  # flake8: noqa

from margarine import queues
from margarine.datastores import get_collection
from margarine.datastores import get_gridfs
from margarine.parameters import PARAMETERS

logger = logging.getLogger(__name__)


class ArticleCreateHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ( 'POST', 'OPTIONS' )

    def write_error(self, status_code, **kwargs):
        pass

    def post(self):
        '''Submit an article.

        :URL: ``/articles/``

        Parameters
        ----------

        :``ARTICLE_URL``: URL of article to add.

        Possible Status Codes
        ---------------------

        :202: Successful submission of article

        Examples
        --------

        1. :request:::
               POST /articles/ HTTP/1.0
               Content-Type: application/x-www-form-urlencoded

               article_url=http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html

           :response:::
               HTTP/1.0 202 Accepted
               Access-Control-Allow-Origin: http://margarine.io
               Location: /articles/44d85795-248d-5899-b8ca-ac2bd8233755

        2. :request:::
               POST /articles/?article_url=http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html HTTP/1.0

           :response:::
               HTTP/1.0 202 Accepted
               Access-Control-Allow-Origin: http://margarine.io
               Location: /articles/44d85795-248d-5899-b8ca-ac2bd8233755

        '''

        article = {}

        article['url'] = self.get_argument('article_url', None)

        logger.info('STARTING: create article %s', article['url'])

        article['uuid'] = uuid.uuid5(uuid.NAMESPACE_URL, article['url'].encode('ascii'))

        with kombu.pools.producers[queues.get_connection()].acquire(block = True) as producer:
            logger.debug('id(producer): %s', id(producer))

            producer.publish(
                article,
                serializer = 'pickle',
                compression = 'bzip2',
                exchange = queues.ARTICLES_TOPIC_EXCHANGE,
                declare = [ queues.ARTICLES_TOPIC_EXCHANGE ],
                routing_key = 'articles.create'
            )

        self.set_status(202)

        self.set_header('Access-Control-Allow-Origin', PARAMETERS['tinge.url'])
        self.set_header('Location', self.reverse_url('read_article', str(article['uuid'])))

        logger.info('STOPPING: create article %s', article['url'])


class ArticleReadHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ( 'GET', 'HEAD', 'OPTIONS' )

    def write_error(self, status_code, **kwargs):
        pass

    def get(self, article_uuid):
        '''Retrieve article data and metadata.

        :URL: ``/articles/{ARTICLE_UUID}``

        Parameters
        ----------

        :``ARTICLE_UUID``: UUID of the article being requested.

        Possible Status Codes
        ---------------------

        :200: Successful retrieval of article
        :404: Article could not be retrieved or did not exist

        Examples
        --------

        1. :request:::
               GET /articles/{ARTICLE_UUID} HTTP/1.0
               [Accept: application/json]

           :response:::
               HTTP/1.0 200 Ok
               Access-Control-Allow-Origin: http://margarine.io
               Content-Type: application/json
               ETag: 21696f99425b45b28ee9d2c308266beb
               Last-Modified: Tue, 15 Nov 1994 12:45:26 GMT
               Link: <http://blog.alunduil.com/posts/singularity-an-alternative-openstack-guest-agent.html>; ref="original"

               {
                 "body": "…Singularity, an Alternative Openstack Guest Agent | Hackery &c…
                 "url": "http://blog.alunduil.com/posts/singularity-an-alternative-openstack-guest-agent.html",
                 "created_at": {"$date": 1374007667571},
                 "etag": "6e2f69536ca15cc18260bffe7583b849",
                 "_id": "03db19bb92205b4fb5fc3c4c0e4b1279",
                 "parsed_at": {"$date": 1374008521414},
                 "size": 9964
               }

        '''

        logger.info('STARTING: read article %s', article_uuid)

        article = get_collection('articles').find_one({ '_id': article_uuid.replace('-', '') })

        logger.debug('article: %s', article)

        if article is None or 'parsed_at' not in article:
            self.send_error(404)
            self.flush()

        if self.request.method == 'HEAD':
            del article['body']
        else:
            article['body'] = get_gridfs().get(article['body']).read()

        def _(obj):
            logger.debug('type(obj): %s', type(obj))
            logger.debug('obj: %s', obj)

            if isinstance(obj, datetime.datetime):
                return pytz.utc.localize(obj).strftime('%a, %d %b %Y %H:%M:%S.%f%z')
            raise TypeError

        self.write(json.dumps(article, default = _))

        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', PARAMETERS['tinge.url'])
        self.set_header('ETag', article['etag'])
        self.set_header('Last-Modified', pytz.utc.localize(article['updated_at']).strftime('%a, %d %b %Y %H:%M:%S %Z'))
        self.set_header('Link', '<{0}>; rel="original"'.format(article['original_url']))

        logger.info('STOPPING: read article %s', article_uuid)

    head = get
