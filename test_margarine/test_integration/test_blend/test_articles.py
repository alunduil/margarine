# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import json
import logging
import urllib

from test_margarine.test_common.test_blend import BaseBlendTest
from test_margarine.test_integration import BaseDatastoreIntegrationTest
from test_margarine.test_integration import BaseQueueIntegrationTest

from margarine import queues

logger = logging.getLogger(__name__)


class BlendArticleReadWithDatastoreTest(BaseBlendTest, BaseDatastoreIntegrationTest):
    mocks_mask = set()
    mocks_mask = mocks_mask.union(BaseBlendTest.mocks_mask)
    mocks_mask = mocks_mask.union(BaseDatastoreIntegrationTest.mocks_mask)

    mocks = set()
    mocks = mocks.union(BaseBlendTest.mocks)
    mocks = mocks.union(BaseDatastoreIntegrationTest.mocks)

    def test_article_read_get_unsubmitted(self):
        '''blend.articles—GET    /articles/? → 404—unmocked datastores,unsubmitted'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'])

            self.assertEqual(404, response.code)
            self.assertEqual(0, len(response.body))

    def test_article_read_head_unsubmitted(self):
        '''blend.articles—HEAD   /articles/? → 404—unmocked datastores,unsubmitted'''

        for article in self.articles['all']:
            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD')

            self.assertEqual(404, response.code)
            self.assertEqual(0, len(response.body))

    def test_article_read_get_submitted_unsanitized(self):
        '''blend.articles—GET    /articles/? → 404—unmocked datastores,submitted,unsanitized'''

        for article in self.articles['all']:
            self.add_fixture_to_datastore(article['bson']['post_create'])

            response = self.fetch(self.base_url + article['uuid'])

            self.assertEqual(404, response.code)
            self.assertEqual(0, len(response.body))

    def test_article_read_head_submitted_unsanitized(self):
        '''blend.articles—HEAD   /articles/? → 404—unmocked datastores,submitted,unsanitized'''

        for article in self.articles['all']:
            self.add_fixture_to_datastore(article['bson']['post_create'])

            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD')

            self.assertEqual(404, response.code)
            self.assertEqual(0, len(response.body))

    def test_article_read_get_submitted_sanitized(self):
        '''blend.articles—GET    /articles/? → 200—ummocked datastores,submitted,sanitized'''

        for article in self.articles['all']:
            _ = {}
            _.update(article['bson']['post_create'])
            _.update(article['bson']['post_sanitize'])
            self.add_fixture_to_datastore(_, article['json']['body'])

            response = self.fetch(self.base_url + article['uuid'])

            self.assertEqual(200, response.code)

            self.assertIsNotNone(response.headers.get('Access-Control-Allow-Origin'))

            self.assertEqual('application/json', response.headers.get('Content-Type'))

            self.assertEqual(article['generated_headers']['etag'], response.headers.get('ETag'))
            self.assertEqual(article['generated_headers']['last_modified'], response.headers.get('Last-Modified'))
            self.assertEqual('<{0}>; rel="original"'.format(article['url']), response.headers.get('Link'))

            _, self.maxDiff = self.maxDiff, None
            self.assertEqual(article['json'], json.loads(response.body))
            self.maxDiff = _

    def test_article_read_head_submitted_sanitized(self):
        '''blend.articles—HEAD   /articles/? → 200—unmocked datastores,submitted,sanitized'''

        for article in self.articles['all']:
            _ = {}
            _.update(article['bson']['post_create'])
            _.update(article['bson']['post_sanitize'])
            self.add_fixture_to_datastore(_, article['json']['body'])

            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD')

            self.assertEqual(200, response.code)

            self.assertIsNotNone(response.headers.get('Access-Control-Allow-Origin'))

            self.assertEqual('application/json', response.headers.get('Content-Type'))

            self.assertEqual(article['generated_headers']['etag'], response.headers.get('ETag'))
            self.assertEqual(article['generated_headers']['last_modified'], response.headers.get('Last-Modified'))
            self.assertEqual('<{0}>; rel="original"'.format(article['url']), response.headers.get('Link'))

            self.assertEqual(0, len(response.body))


class BlendArticleCreateWithQueueTest(BaseBlendTest, BaseQueueIntegrationTest):
    mocks_mask = set()
    mocks_mask = mocks_mask.union(BaseBlendTest.mocks_mask)
    mocks_mask = mocks_mask.union(BaseQueueIntegrationTest.mocks_mask)

    mocks = set()
    mocks = mocks.union(BaseBlendTest.mocks)
    mocks = mocks.union(BaseQueueIntegrationTest.mocks)

    def test_article_create_message_sent(self):
        '''blend.articles—POST   /articles/ → 202—unmocked queues,message submitted'''

        for article in self.articles['all']:
            self.fetch(self.base_url, method = 'POST', body = urllib.urlencode({ 'article_url': article['url'] }))

            self.assertEqual(article['message_body']['pre_create'], self.intercept_message(queues.ARTICLES_CREATE_QUEUE))
