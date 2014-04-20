# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_margarine.test_common.test_spread import BaseSpreadTest
from test_margarine.test_integration import BaseDatastoreIntegrationTest
from test_margarine.test_integration import BaseQueueIntegrationTest

from margarine import datastores
from margarine import queues
from margarine.spread.articles import create_article


class SpreadArticleCreateWithDatastoreTest(BaseSpreadTest, BaseDatastoreIntegrationTest):
    mocks_mask = set()
    mocks_mask = mocks_mask.union(BaseSpreadTest.mocks_mask)
    mocks_mask = mocks_mask.union(BaseDatastoreIntegrationTest.mocks_mask)

    mocks = set()
    mocks = mocks.union(BaseSpreadTest.mocks)
    mocks = mocks.union(BaseDatastoreIntegrationTest.mocks)

    def test_article_create_uncreated(self):
        '''spread.articles—create—unmocked datastores,uncreated'''

        for article in self.articles['all']:
            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['post_create']['created_at'],
                    article['bson']['post_create']['updated_at'],
                ]

            self.mock_queues()

            create_article(article['message_body']['pre_create'], self.mocked_message)

            _, self.maxDiff = self.maxDiff, None
            self.assertEqual(article['bson']['post_create'], datastores.get_collection('articles').find_one(article['uuid'].replace('-', '')))
            self.maxDiff = _

    def test_article_create_created(self):
        '''spread.articles—create—unmocked datastores,created'''

        for article in self.articles['all']:
            self.add_fixture_to_datastore(article['bson']['post_create'])

            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['post_create']['created_at'],
                    article['bson']['post_create']['updated_at'],
                ]

            self.mock_queues()

            create_article(article['message_body']['pre_create'], self.mocked_message)

            self.assertEqual(article['bson']['post_create'], datastores.get_collection('articles').find_one(article['uuid'].replace('-', '')))


class SpreadArticleCreateWithQueueTest(BaseSpreadTest, BaseQueueIntegrationTest):
    mocks_mask = set()
    mocks_mask = mocks_mask.union(BaseSpreadTest.mocks_mask)
    mocks_mask = mocks_mask.union(BaseQueueIntegrationTest.mocks_mask)

    mocks = set()
    mocks = mocks.union(BaseSpreadTest.mocks)
    mocks = mocks.union(BaseQueueIntegrationTest.mocks)

    def test_article_create_message_sent(self):
        '''spread.articles—create—unmocked queues,message submitted'''

        for article in self.articles['all']:
            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['post_create']['created_at'],
                    article['bson']['post_create']['updated_at'],
                ]

            if self.mock_datastores():
                self.mocked_collection.find_one.return_value = None

            create_article(article['message_body']['pre_create'], self.mocked_message)

            self.assertEqual(article['message_body']['post_create'], self.intercept_message(queues.ARTICLES_SANITIZE_QUEUE))
