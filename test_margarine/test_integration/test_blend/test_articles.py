# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import json
import logging
import unittest

from test_margarine import test_helpers
from test_margarine.test_common.test_blend import BaseBlendTest
from test_margarine.test_integration import BaseMargarineIntegrationTest

logger = logging.getLogger(__name__)


@unittest.skipUnless(test_helpers.is_vagrant_up('datastore'), 'vagrant up datastore')
class BlendArticleReadWithDatastoreTest(BaseBlendTest, BaseMargarineIntegrationTest):
    mocks_mask = set()
    mocks_mask = mocks_mask.union(BaseBlendTest.mocks_mask)
    mocks_mask = mocks_mask.union(BaseMargarineIntegrationTest.mocks_mask)

    mocks = set()
    mocks = mocks.union(BaseBlendTest.mocks)
    mocks = mocks.union(BaseMargarineIntegrationTest.mocks)

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

    def test_article_read_get_submitted_incomplete(self):
        '''blend.articles—GET    /articles/? → 404—unmocked datastores,submitted,incomplete'''

        for article in self.articles['all']:
            del article['bson']['parsed_at']

            self.add_fixture_to_datastore(article)

            response = self.fetch(self.base_url + article['uuid'])

            self.assertEqual(404, response.code)
            self.assertEqual(0, len(response.body))

    def test_article_read_head_submitted_incomplete(self):
        '''blend.articles—HEAD   /articles/? → 404—unmocked datastores,submitted,incomplete'''

        for article in self.articles['all']:
            del article['bson']['parsed_at']

            self.add_fixture_to_datastore(article)

            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD')

            self.assertEqual(404, response.code)
            self.assertEqual(0, len(response.body))

    def test_article_read_get_submitted_complete(self):
        '''blend.articles—GET    /articles/? → 200—ummocked datastores,submitted,complete'''

        for article in self.articles['all']:
            self.add_fixture_to_datastore(article)

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
        '''blend.articles—HEAD   /articles/? → 200—unmocked datastores,submitted,complete'''

        for article in self.articles['all']:
            self.add_fixture_to_datastore(article)

            response = self.fetch(self.base_url + article['uuid'], method = 'HEAD')

            self.assertEqual(200, response.code)

            self.assertIsNotNone(response.headers.get('Access-Control-Allow-Origin'))

            self.assertEqual('application/json', response.headers.get('Content-Type'))

            self.assertEqual(article['etag'], response.headers.get('ETag'))
            self.assertEqual(article['updated_at'], response.headers.get('Last-Modified'))
            self.assertEqual('<{0}>; rel="original"'.format(article['url']), response.headers.get('Link'))

            self.assertEqual(0, len(response.body))
