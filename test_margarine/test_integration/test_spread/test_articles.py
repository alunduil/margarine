# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import bson.objectid
import mock
import unittest

from test_margarine import test_helpers
from test_margarine.test_common.test_spread import BaseSpreadTest
from test_margarine.test_integration import BaseMargarineIntegrationTest

from margarine import datastores
from margarine import queues
from margarine.spread.articles import create_article
from margarine.spread.articles import sanitize_article


@unittest.skipUnless(test_helpers.is_vagrant_up('datastore'), 'vagrant up datastore')
class SpreadArticleCreateWithDatastoreTest(BaseSpreadTest, BaseMargarineIntegrationTest):
    mocks_mask = set()
    mocks_mask = mocks_mask.union(BaseSpreadTest.mocks_mask)
    mocks_mask = mocks_mask.union(BaseMargarineIntegrationTest.mocks_mask)

    mocks = set()
    mocks = mocks.union(BaseSpreadTest.mocks)
    mocks = mocks.union(BaseMargarineIntegrationTest.mocks)

    def test_article_create_uncreated(self):
        '''spread.articles—create—unmocked datastores,uncreated'''

        for article in self.articles['all']:
            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['post_create']['created_at'],
                    article['bson']['post_create']['updated_at'],
                ]

            is_queue_mocked = self.mock_queues()

            create_article(article['message_body']['pre_create'], self.mocked_message)

            _, self.maxDiff = self.maxDiff, None
            self.assertEqual(article['bson']['post_create'], datastores.get_collection('articles').find_one(article['uuid'].replace('-', '')))
            self.maxDiff = _

            if is_queue_mocked:
                self.mocked_producer.publish.assert_called_once_with(
                    article['message_body']['post_create'],
                    serializer = mock.ANY,
                    compression = mock.ANY,
                    exchange = queues.ARTICLES_FANOUT_EXCHANGE,
                    declare = [ queues.ARTICLES_FANOUT_EXCHANGE ],
                    routing_key = 'articles.secondary'
                )

            self.mocked_message.ack.assert_called_once_with()

    def test_article_create_created(self):
        '''spread.articles—create—unmocked datastores,created'''

        for article in self.articles['all']:
            self.add_fixture_to_datastore(article['bson']['post_create'])

            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['post_create']['created_at'],
                    article['bson']['post_create']['updated_at'],
                ]

            is_queue_mocked = self.mock_queues()

            create_article(article['message_body']['pre_create'], self.mocked_message)

            self.assertEqual(article['bson']['post_create'], datastores.get_collection('articles').find_one(article['uuid'].replace('-', '')))

            if is_queue_mocked:
                self.mocked_producer.publish.assert_called_once_with(
                    article['message_body']['post_create'],
                    serializer = mock.ANY,
                    compression = mock.ANY,
                    exchange = queues.ARTICLES_FANOUT_EXCHANGE,
                    declare = [ queues.ARTICLES_FANOUT_EXCHANGE ],
                    routing_key = 'articles.secondary'
                )

            self.mocked_message.ack.assert_called_once_with()


@unittest.skipUnless(test_helpers.is_vagrant_up('datastore'), 'vagrant up datastore')
class SpreadArticleSanitizeWithDatastoreTest(BaseSpreadTest, BaseMargarineIntegrationTest):
    mocks_mask = set()
    mocks_mask = mocks_mask.union(BaseSpreadTest.mocks_mask)
    mocks_mask = mocks_mask.union(BaseMargarineIntegrationTest.mocks_mask)

    mocks = set()
    mocks = mocks.union(BaseSpreadTest.mocks)
    mocks = mocks.union(BaseMargarineIntegrationTest.mocks)

    def test_article_sanitize_unsanitized(self):
        '''spread.articles—sanitize—unmocked datastores,unsanitized'''

        for article in self.articles['all']:
            if self.mock_tornado():
                headers = {
                    'ETag': article['response']['etag'],
                }

                self.mocked_response.headers.__getitem__.side_effect = lambda _: headers[_]

                type(self.mocked_response).buffer = mock.PropertyMock(return_value = article['response']['html'])

            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['post_sanitize']['parsed_at'],
                    article['bson']['post_sanitize']['updated_at'],
                ]

                self.add_fixture_to_datastore(article['bson']['post_create'], article['bson']['post_sanitize']['body'])

            sanitize_article(article['message_body']['post_create'], self.mocked_message)

            _ = {}
            _.update(article['bson']['post_create'])
            _.update(article['bson']['post_sanitize'])

            result = datastores.get_collection('articles').find_one(article['uuid'].replace('-', ''))

            self.assertIsInstance(result['body'], bson.objectid.ObjectId)
            self.assertEqual(_, result)

            self.mocked_message.ack.assert_called_once_with()

    def test_article_sanitize_sanitized_unmodified(self):
        '''spread.articles—sanitize—unmocked datastores,sanitized,unmodified'''

        for article in self.articles['all']:
            if self.mock_tornado():
                headers = {
                    'ETag': article['response']['etag']
                }

                self.mocked_response.headers.__getitem__.side_effect = lambda _: headers[_]

                type(self.mocked_response).buffer = mock.PropertyMock(return_value = article['response']['html'])

            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['post_sanitize']['parsed_at'],
                    article['bson']['post_sanitize']['updated_at'],
                ]

            _ = {}
            _.update(article['bson']['post_create'])
            _.update(article['bson']['post_sanitize'])
            self.add_fixture_to_datastore(_)

            sanitize_article(article['message_body']['post_create'], self.mocked_message)

            _ = {}
            _.update(article['bson']['post_create'])
            _.update(article['bson']['post_sanitize'])

            self.assertEqual(_, datastores.get_collection('articles').find_one(article['uuid'].replace('-', '')))

            self.mocked_message.ack.assert_called_once_with()

    def test_article_sanitize_sanitized_modified(self):
        '''spread.articles—sanitize—unmocked datastores,sanitized,modified'''

        for article in self.articles['all']:
            if self.mock_tornado():
                headers = {
                    'ETag': 'd0dbbb6ba01a95c3bfeca3f46e3d15b',
                }

                self.mocked_response.headers.__getitem__.side_effect = lambda _: headers[_]

                type(self.mocked_response).buffer = mock.PropertyMock(return_value = article['response']['html'])

            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['post_sanitize']['parsed_at'],
                    article['bson']['post_sanitize']['updated_at'],
                ]

            _ = {}
            _.update(article['bson']['post_create'])
            _.update(article['bson']['post_sanitize'])
            self.add_fixture_to_datastore(_, article['bson']['post_sanitize']['body'])

            sanitize_article(article['message_body']['post_create'], self.mocked_message)

            _ = {}
            _.update(article['bson']['post_create'])
            _.update(article['bson']['post_sanitize'])
            _[u'previous_bodies'] = [ _['body'] ]
            _[u'etag'] = u'3ddd80984969be128d91d752f198a6006dbbb162ebdd9d0589aea85f3b1fdbb4'
            _[u'original_etag'] = u'd0dbbb6ba01a95c3bfeca3f46e3d15b'

            self.maxDiff = None
            self.assertEqual(_, datastores.get_collection('articles').find_one(article['uuid'].replace('-', '')))

            self.mocked_message.ack.assert_called_once_with()
