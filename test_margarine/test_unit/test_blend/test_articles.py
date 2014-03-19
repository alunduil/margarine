# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import json
import logging
import mock
import tornado.testing
import uuid

from test_margarine.test_fixtures.test_articles import ARTICLES
from test_margarine.test_unit.test_blend import BaseBlendTest

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

        self.articles = copy.deepcopy(ARTICLES)

        self.base_url = '/{i.API_VERSION}/articles/'.format(i = information)

    mocks.add('datastores.get_collection')

    def mock_datastore(self):
        if 'datastores.get_collection' in self.mocks_mask:
            return False

        _ = mock.patch('margarine.blend.articles.get_collection')

        self.addCleanup(_.stop)

        self.mocked_datastore = _.start()

        self.mocked_collection = mock.MagicMock()
        self.mocked_datastore.return_value = self.mocked_collection

        return True

    mocks.add('datastores.get_container')

    def mock_pyrax(self):
        if 'datastores.get_container' in self.mocks_mask:
            return False

        _ = mock.patch('margarine.blend.articles.get_container')

        self.addCleanup(_.stop)

        self.mocked_pyrax = _.start()

        self.mocked_container = mock.MagicMock()
        self.mocked_pyrax.return_value = self.mocked_container

        self.mocked_object = mock.MagicMock()
        self.mocked_container.get_object.return_value = self.mocked_object

        return True

    def test_article_read_delete(self):
        '''blend.articles—DELETE /articles/? → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'DELETE')

            self.assertEqual(405, response.code)

    def test_article_read_patch(self):
        '''blend.articles—PATCH /articles/? → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'PATCH', body = '')

            self.assertEqual(405, response.code)

    def test_article_read_put(self):
        '''blend.articles—PUT /articles/? → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'PUT', body = '')

            self.assertEqual(405, response.code)

    def test_article_read_post(self):
        '''blend.articles—POST /articles/? → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'POST', body = '')

            self.assertEqual(405, response.code)

    def test_article_read_get_unsubmitted(self):
        '''blend.articles—GET /articles/? → 404—unsubmitted'''

        self.mock_datastore()

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'])

            self.assertEqual(404, response.code)

    def test_article_read_head_unsubmitted(self):
        '''blend.articles—HEAD /articles/? → 404—unsubmitted'''

        self.mock_datastore()

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD')

            self.assertEqual(404, response.code)

    def test_article_read_get_submitted_incomplete(self):
        '''blend.articles—GET /articles/? → 404—submitted,incomplete'''

        for article in self.articles['all']:
            del article['bson']['parsed_at']

            if self.mock_datastore():
                self.mocked_collection.find_one.return_value = article['bson']

            response = self.fetch(self.base_url + article['uuid'])

            self.assertEqual(404, response.code)

    def test_article_read_head_submitted_incomplete(self):
        '''blend.articles—HEAD /articles/? → 404—submitted,incomplete'''

        for article in self.articles['all']:
            del article['bson']['parsed_at']

            if self.mock_datastore():
                self.mocked_collection.find_one.return_value = article['bson']

            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD')

            self.assertEqual(404, response.code)

    def test_article_read_get_submitted_complete(self):
        '''blend.articles—GET /articles/? → 200—submitted,complete'''

        for article in self.articles['all']:
            if self.mock_datastore():
                self.mocked_collection.find_one.return_value = article['bson']

            if self.mock_pyrax():
                self.mocked_object.fetch.return_value = article['json']['body']

            response = self.fetch(self.base_url + article['uuid'])

            self.assertEqual(200, response.code)

            self.assertIsNotNone(response.headers.get('Access-Control-Allow-Origin'))

            self.assertEqual('application/json', response.headers.get('Content-Type'))

            self.assertEqual(article['etag'], response.headers.get('ETag'))
            self.assertEqual(article['updated_at'], response.headers.get('Last-Modified'))
            self.assertEqual('<{0}>; rel="original"'.format(article['url']), response.headers.get('Link'))

            _, self.maxDiff = self.maxDiff, None
            self.assertEqual(article['json'], json.loads(response.body))
            self.maxDiff = _

    def test_article_read_head_submitted_complete(self):
        '''blend.articles—HEAD /articles/? → 200—submitted,complete'''

        for article in self.articles['all']:
            if self.mock_datastore():
                self.mocked_collection.find_one.return_value = article['bson']

            if self.mock_pyrax():
                self.mocked_object.fetch.return_value = article['json']['body']

            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD')

            self.assertEqual(200, response.code)

            self.assertIsNotNone(response.headers.get('Access-Control-Allow-Origin'))

            self.assertEqual('application/json', response.headers.get('Content-Type'))

            self.assertEqual(article['etag'], response.headers.get('ETag'))
            self.assertEqual(article['updated_at'], response.headers.get('Last-Modified'))
            self.assertEqual('<{0}>; rel="original"'.format(article['url']), response.headers.get('Link'))


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
