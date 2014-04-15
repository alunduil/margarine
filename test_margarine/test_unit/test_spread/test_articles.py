# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import mock
import logging

from test_margarine.test_common.test_spread import BaseSpreadTest

from margarine import queues
from margarine.spread.articles import create_article
from margarine.spread.articles import sanitize_article

logger = logging.getLogger(__name__)


class SpreadArticleCreateTest(BaseSpreadTest):
    mocks_mask = set().union(BaseSpreadTest.mocks_mask)
    mocks = set().union(BaseSpreadTest.mocks)

    def test_article_create_uncreated(self):
        '''spread.articles—create—uncreated'''

        for article in self.articles['all']:
            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['post_create']['created_at'],
                    article['bson']['post_create']['updated_at'],
                ]

            is_datastore_mocked = self.mock_datastores()
            if is_datastore_mocked:
                self.mocked_collection.find_one.return_value = None

            is_queue_mocked = self.mock_queues()

            create_article(article['message_body']['pre_create'], self.mocked_message)

            _id = article['bson']['post_create'].pop('_id')

            if is_datastore_mocked:
                self.mocked_collection.update.assert_called_once_with(
                    { '_id': _id, },
                    { '$set': article['bson']['post_create'] },
                    upsert = True
                )

            if is_queue_mocked:
                self.mocked_ensure.assert_called_once_with(
                    article['message_body']['post_create'],
                    serializer = mock.ANY,
                    compression = mock.ANY,
                    exchange = queues.ARTICLES_FANOUT_EXCHANGE,
                    declare = [ queues.ARTICLES_FANOUT_EXCHANGE ],
                    routing_key = 'articles.secondary'
                )

            self.mocked_message.ack.assert_called_once_with()

    def test_article_create_created(self):
        '''spread.articles—create—created'''

        for article in self.articles['all']:
            is_datastore_mocked = self.mock_datastores()
            if is_datastore_mocked:
                self.mocked_collection.find_one.return_value = copy.deepcopy(article['bson']['post_create'])

            is_queue_mocked = self.mock_queues()

            create_article(article['message_body']['pre_create'], self.mocked_message)

            _id = article['bson']['post_create'].pop('_id')

            if is_datastore_mocked:
                self.mocked_collection.update.assert_called_once_with(
                    { '_id': _id },
                    { '$set': article['bson']['post_create'] },
                    upsert = True
                )

            if is_queue_mocked:
                self.mocked_ensure.assert_called_once_with(
                    article['message_body']['post_create'],
                    serializer = mock.ANY,
                    compression = mock.ANY,
                    exchange = queues.ARTICLES_FANOUT_EXCHANGE,
                    declare = [ queues.ARTICLES_FANOUT_EXCHANGE ],
                    routing_key = 'articles.secondary'
                )

            self.mocked_message.ack.assert_called_once_with()


class SpreadArticleSanitizeTest(BaseSpreadTest):
    mocks_mask = set().union(BaseSpreadTest.mocks_mask)
    mocks = set().union(BaseSpreadTest.mocks)

    def test_article_sanitize_unsanitized(self):
        '''spread.articles—sanitize—not sanitized'''

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

            is_datastore_mocked = self.mock_datastores()
            if is_datastore_mocked:
                self.mocked_collection.find_one.return_value = copy.deepcopy(article['bson']['post_create'])
                self.mocked_gridfs.put.return_value = article['bson']['post_sanitize']['body']

            sanitize_article(article['message_body']['post_create'], self.mocked_message)

            _ = {}
            _.update(article['bson']['post_create'])
            _.update(article['bson']['post_sanitize'])

            _id = _.pop('_id')

            if is_datastore_mocked:
                self.mocked_collection.update.assert_called_once_with({ '_id': _id }, { '$set': _ }, upsert = True)

            self.mocked_message.ack.assert_called_once_with()

    def test_article_sanitize_sanitized_unmodified(self):
        '''spread.articles—sanitize—sanitized,unmodified'''

        for article in self.articles['all']:
            if self.mock_tornado():
                headers = {
                    'ETag': article['response']['etag'],
                }

                self.mocked_response.headers.__getitem__.side_effect = lambda _: headers[_]

                type(self.mocked_response).buffer = mock.PropertyMock(return_value = article['response']['html']),

            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['post_sanitize']['parsed_at'],
                    article['bson']['post_sanitize']['updated_at'],
                ]

            is_datastore_mocked = self.mock_datastores()
            if is_datastore_mocked:
                _ = {}
                _.update(article['bson']['post_create'])
                _.update(article['bson']['post_sanitize'])
                self.mocked_collection.find_one.return_value = _

            sanitize_article(article['message_body']['post_create'], self.mocked_message)

            if is_datastore_mocked:
                self.assertFalse(self.mocked_collection.update.called)

            self.mocked_message.ack.assert_called_once_with()

    def test_article_sanitize_sanitized_modified(self):
        '''spread.articles—sanitize—sanitized,modified'''

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

            is_datastore_mocked = self.mock_datastores()
            if is_datastore_mocked:
                _ = {}
                _.update(article['bson']['post_create'])
                _.update(article['bson']['post_sanitize'])
                self.mocked_collection.find_one.return_value = _
                self.mocked_gridfs.put.return_value = article['bson']['post_sanitize']['body']

            sanitize_article(article['message_body']['post_create'], self.mocked_message)

            _ = {}
            _.update(article['bson']['post_create'])
            _.update(article['bson']['post_sanitize'])
            _['previous_bodies'] = [ _['body'] ]
            _['etag'] = '3ddd80984969be128d91d752f198a6006dbbb162ebdd9d0589aea85f3b1fdbb4'
            _['original_etag'] = 'd0dbbb6ba01a95c3bfeca3f46e3d15b'

            _id = _.pop('_id')

            if is_datastore_mocked:
                self.mocked_collection.update.assert_called_once_with({ '_id': _id }, { '$set': _ }, upsert = True)

            self.mocked_message.ack.assert_called_once_with()
