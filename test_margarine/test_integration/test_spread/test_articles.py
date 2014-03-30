# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import mock
import unittest
import uuid

from test_margarine import test_helpers
from test_margarine.test_common.test_spread import BaseSpreadTest
from test_margarine.test_integration import BaseMargarineIntegrationTest

from margarine import datastores
from margarine import queues
from margarine.spread.articles import create_article


@unittest.skipUnless(test_helpers.is_vagrant_up('datastore'), 'vagrant up datastore')
class SpreadArticleCreateWithDatastoreTest(BaseSpreadTest, BaseMargarineIntegrationTest):
    mocks_mask = set()
    mocks_mask = mocks_mask.union(BaseSpreadTest.mocks_mask)
    mocks_mask = mocks_mask.union(BaseMargarineIntegrationTest.mocks_mask)

    mocks = set()
    mocks = mocks.union(BaseSpreadTest.mocks)
    mocks = mocks.union(BaseMargarineIntegrationTest.mocks)

    def test_article_create_unsubmitted(self):
        '''spread.articles—create—unmocked datastores,unsubmitted'''

        for article in self.articles['all']:
            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['created_at'],
                    article['bson']['updated_at'],
                ]

            is_queue_mocked = self.mock_queues()

            create_article(article['message_body'], self.mocked_message)

            del article['bson']['body']
            del article['bson']['etag']
            del article['bson']['parsed_at']

            _, self.maxDiff = self.maxDiff, None
            self.assertEqual(article['bson'], datastores.get_collection('articles').find_one(article['message_body']['uuid'].hex))
            self.maxDiff = _

            if is_queue_mocked:
                self.mocked_producer.publish.assert_called_once_with(
                    { 'uuid': uuid.UUID(article['uuid']) },
                    serializer = mock.ANY,
                    compression = mock.ANY,
                    exchange = queues.ARTICLES_FANOUT_EXCHANGE,
                    declare = [ queues.ARTICLES_FANOUT_EXCHANGE ],
                    routing_key = 'articles.secondary'
                )

            self.mocked_message.ack.assert_called_once_with()

    def test_article_create_submitted(self):
        '''spread.articles—create—unmocked datastores,submitted'''

        for article in self.articles['all']:
            self.add_fixture_to_datastore(article)

            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['created_at'],
                    article['bson']['updated_at'],
                ]

            is_queue_mocked = self.mock_queues()

            create_article(article['message_body'], self.mocked_message)

            self.assertEqual(article['bson'], datastores.get_collection('articles').find_one(article['message_body']['uuid'].hex))

            if is_queue_mocked:
                self.mocked_producer.publish.assert_called_once_with(
                    { 'uuid': uuid.UUID(article['uuid']) },
                    serializer = mock.ANY,
                    compression = mock.ANY,
                    exchange = queues.ARTICLES_FANOUT_EXCHANGE,
                    declare = [ queues.ARTICLES_FANOUT_EXCHANGE ],
                    routing_key = 'articles.secondary'
                )

            self.mocked_message.ack.assert_called_once_with()
