# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import datetime
import json
import logging
import mock
import tornado.testing
import uuid
import unittest

from test_margarine.test_fixtures.test_articles import ARTICLES
from test_margarine.test_unit.test_blend import BaseBlendTest

from margarine.blend import BLEND
from margarine.blend import BLEND_APPLICATION
from margarine.blend import information

logger = logging.getLogger(__name__)


class BlendArticleReadTest(tornado.testing.AsyncHTTPTestCase):
    mocks_mask = set()
    mocks = set()

    def get_app(self):
        return BLEND_APPLICATION

    def setUp(self):
        super(BlendArticleReadTest, self).setUp()

        articles_copy = copy.copy(ARTICLES)
        def _():
            ARTICLES = articles_copy
        self.addCleanup(_)

        self.base_url = '/{i.API_VERSION}/articles/'.format(i = information)

    mocks.add('datastores.get_container')
    def mock_pyrax(self):
        if 'datastores.get_container' in self.mocks_mask:
            return

        _ = mock.patch('margarine.blend.articles.get_container')

        self.addCleanup(_.stop)

        self.mocked_pyrax = _.start()

        self.mocked_container = mock.MagicMock()
        self.mocked_pyrax.return_value = self.mocked_container

        self.mocked_object = mock.MagicMock()
        self.mocked_container.get_object.return_value = self.mocked_object

    def test_article_read_delete(self):
        '''blend.articles—DELETE /articles/? → 405'''

        for article in ARTICLES['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'DELETE')

            self.assertEqual(405, response.code)

    def test_article_read_get(self):
        '''blend.articles—GET /articles/? → 301'''

        for article in ARTICLES['all']:
            self.mock_pyrax()

            mocked_cdn_uri = mock.PropertyMock(return_value = article['cdn_uri'])
            type(self.mocked_container).cdn_uri = mocked_cdn_uri

            response = self.fetch(self.base_url + article['uuid'], follow_redirects = False)

            logger.debug('error: %s', response.error)

            self.assertEqual(301, response.code)
            self.assertEqual('/'.join([ article['cdn_uri'], 'articles', article['uuid'] ]), response.headers.get('Location', ''))

    def test_article_read_head(self):
        '''blend.articles—HEAD /articles/? → 301'''

        for article in ARTICLES['all']:
            self.mock_pyrax()

            mocked_cdn_uri = mock.PropertyMock(return_value = article['cdn_uri'])
            type(self.mocked_container).cdn_uri = mocked_cdn_uri

            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD', follow_redirects = False)

            logger.debug('error: %s', response.error)

            self.assertEqual(301, response.code)
            self.assertEqual('/'.join([ article['cdn_uri'], 'articles', article['uuid'] ]), response.headers.get('Location', ''))

    def test_article_read_patch(self):
        '''blend.articles—PATCH /articles/? → 405'''

        for article in ARTICLES['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'PATCH', body = '')

            logger.debug('error: %s', response.error)

            self.assertEqual(405, response.code)

    def test_article_read_put(self):
        '''blend.articles—PUT /articles/? → 405'''

        for article in ARTICLES['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'PUT', body = '')

            logger.debug('error: %s', response.error)

            self.assertEqual(405, response.code)

    def test_article_read_post(self):
        '''blend.articles—POST /articles/? → 405'''

        for article in ARTICLES['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'POST', body = '')

            logger.debug('error: %s', response.error)

            self.assertEqual(405, response.code)


class BaseBlendArticleTest(BaseBlendTest):
    # TODO Make this simpler.
    mock_mask = BaseBlendTest.mock_mask | set(['keyspace'])

    def setUp(self):
        super(BaseBlendArticleTest, self).setUp()

        self.articles = [
                'http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html',
                'http://developer.rackspace.com/blog/got-python-questions.html',
                ]

        self.articles = dict([ (uuid.uuid5(uuid.NAMESPACE_URL, _), _) for _ in self.articles ])

        self.base_url = '/{i.API_VERSION}/articles/'.format(i = information)

class BlendArticleCreateTest(BaseBlendArticleTest):
    def test_article_create(self):
        '''Blend::Article Create'''

        for uuid, url in self.articles.iteritems():
            response = self.application.post(self.base_url, data = {
                'url': url,
                })

            self.mock_channel.basic_publish.assert_called_once_with(
                    body = '{"url": "' + url + '", "_id": "' + uuid.hex + '"}',
                    exchange = 'margarine.articles.topic',
                    properties = mock.ANY,
                    routing_key = 'articles.create'
                    )

            self.mock_channel.reset_mock()

            self.assertIn('202', response.status)

            #self.assertIn(self.base_url + str(uuid), response.headers.get('Location'))

