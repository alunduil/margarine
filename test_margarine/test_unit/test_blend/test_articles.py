# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import json
import logging
import mock
import urllib

from test_margarine.test_common.test_blend import BaseBlendTest

from margarine import queues

logger = logging.getLogger(__name__)


class BlendArticleCreateTest(BaseBlendTest):
    mocks_mask = set().union(BaseBlendTest.mocks_mask)
    mocks = set().union(BaseBlendTest.mocks)

    def test_article_create_delete(self):
        '''blend.articles—DELETE /articles/ → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url, method = 'DELETE')

            self.assertEqual(405, response.code)

    def test_article_create_patch(self):
        '''blend.articles—PATCH  /articles/ → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url, method = 'PATCH', body = '')

            self.assertEqual(405, response.code)

    def test_article_create_put(self):
        '''blend.articles—PUT    /articles/ → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url, method = 'PUT', body = '')

            self.assertEqual(405, response.code)

    def test_article_create_get(self):
        '''blend.articles—GET    /articles/ → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url)

            self.assertEqual(405, response.code)

    def test_article_create_head(self):
        '''blend.articles—HEAD   /articles/ → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url, method = 'HEAD')

            self.assertEqual(405, response.code)

    def test_article_create_post(self):
        '''blend.articles—POST   /articles/ → 202'''

        for article in self.articles['all']:
            is_queues_mocked = self.mock_queues()

            response = self.fetch(self.base_url, method = 'POST', body = urllib.urlencode({ 'article_url': article['url'] }))

            self.assertEqual(202, response.code)

            self.assertIsNotNone(response.headers.get('Access-Control-Allow-Origin'))

            self.assertEqual(self.base_url + article['uuid'], response.headers.get('Location'))

            if is_queues_mocked:
                self.mocked_producer.publish.assert_called_once_with(
                    article['message_body'],
                    serializer = mock.ANY,
                    compression = mock.ANY,
                    exchange = queues.ARTICLES_TOPIC_EXCHANGE,
                    declare = [ queues.ARTICLES_TOPIC_EXCHANGE ],
                    routing_key = 'articles.create'
                )


class BlendArticleReadTest(BaseBlendTest):
    mocks_mask = set().union(BaseBlendTest.mocks_mask)
    mocks = set().union(BaseBlendTest.mocks)

    def test_article_read_delete(self):
        '''blend.articles—DELETE /articles/? → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'DELETE')

            self.assertEqual(405, response.code)

    def test_article_read_patch(self):
        '''blend.articles—PATCH  /articles/? → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'PATCH', body = '')

            self.assertEqual(405, response.code)

    def test_article_read_put(self):
        '''blend.articles—PUT    /articles/? → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'PUT', body = '')

            self.assertEqual(405, response.code)

    def test_article_read_post(self):
        '''blend.articles—POST   /articles/? → 405'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'POST', body = '')

            self.assertEqual(405, response.code)

    def test_article_read_get_unsubmitted(self):
        '''blend.articles—GET    /articles/? → 404—unsubmitted'''

        self.mock_datastores()

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'])

            self.assertEqual(404, response.code)
            self.assertEqual(0, len(response.body))

    def test_article_read_head_unsubmitted(self):
        '''blend.articles—HEAD   /articles/? → 404—unsubmitted'''

        self.mock_datastores()

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD')

            self.assertEqual(404, response.code)
            self.assertEqual(0, len(response.body))

    def test_article_read_get_submitted_incomplete(self):
        '''blend.articles—GET    /articles/? → 404—submitted,incomplete'''

        for article in self.articles['all']:
            del article['bson']['parsed_at']

            if self.mock_datastores():
                self.mocked_collection.find_one.return_value = article['bson']

            response = self.fetch(self.base_url + article['uuid'])

            self.assertEqual(404, response.code)
            self.assertEqual(0, len(response.body))

    def test_article_read_head_submitted_incomplete(self):
        '''blend.articles—HEAD   /articles/? → 404—submitted,incomplete'''

        for article in self.articles['all']:
            del article['bson']['parsed_at']

            if self.mock_datastores():
                self.mocked_collection.find_one.return_value = article['bson']

            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD')

            self.assertEqual(404, response.code)
            self.assertEqual(0, len(response.body))

    def test_article_read_get_submitted_complete(self):
        '''blend.articles—GET    /articles/? → 200—submitted,complete'''

        for article in self.articles['all']:
            if self.mock_datastores():
                self.mocked_collection.find_one.return_value = article['bson']

                _ = mock.MagicMock()
                self.mocked_gridfs.get.return_value = _
                _.read.return_value = article['json']['body']

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
        '''blend.articles—HEAD   /articles/? → 200—submitted,complete'''

        for article in self.articles['all']:
            if self.mock_datastores():
                self.mocked_collection.find_one.return_value = article['bson']

                _ = mock.MagicMock()
                self.mocked_gridfs.get.return_value = _
                _.read.return_value = article['json']['body']

            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD')

            self.assertEqual(200, response.code)

            self.assertIsNotNone(response.headers.get('Access-Control-Allow-Origin'))

            self.assertEqual('application/json', response.headers.get('Content-Type'))

            self.assertEqual(article['etag'], response.headers.get('ETag'))
            self.assertEqual(article['updated_at'], response.headers.get('Last-Modified'))
            self.assertEqual('<{0}>; rel="original"'.format(article['url']), response.headers.get('Link'))

            self.assertEqual(0, len(response.body))
