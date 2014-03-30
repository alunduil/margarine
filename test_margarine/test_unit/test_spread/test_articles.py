# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import mock
import logging
import uuid

from test_margarine.test_common.test_spread import BaseSpreadTest

from margarine import queues
from margarine.spread.articles import create_article
from margarine.spread.articles import sanitize_article

logger = logging.getLogger(__name__)


class SpreadArticleCreateTest(BaseSpreadTest):
    mocks_mask = set().union(BaseSpreadTest.mocks_mask)
    mocks = set().union(BaseSpreadTest.mocks)

    def test_article_create_unsubmitted(self):
        '''spread.articles—create—unsubmitted'''

        for article in self.articles['all']:
            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['created_at'],
                    article['bson']['updated_at'],
                ]

            is_datastore_mocked = self.mock_datastores()
            if is_datastore_mocked:
                self.mocked_collection.find_one.return_value = None

            is_queue_mocked = self.mock_queues()

            create_article(article['message_body'], self.mocked_message)

            del article['bson']['_id']
            del article['bson']['body']
            del article['bson']['etag']
            del article['bson']['parsed_at']

            if is_datastore_mocked:
                self.mocked_collection.update.assert_called_once_with(
                    { '_id': article['uuid'].replace('-', '') },
                    { '$set': article['bson'] },
                    upsert = True
                )

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
        '''spread.articles—create—submitted'''

        for article in self.articles['all']:
            is_datastore_mocked = self.mock_datastores()
            if is_datastore_mocked:
                self.mocked_collection.find_one.return_value = copy.deepcopy(article['bson'])

            is_queue_mocked = self.mock_queues()

            create_article(article['message_body'], self.mocked_message)

            del article['bson']['_id']

            if is_datastore_mocked:
                self.mocked_collection.update.assert_called_once_with(
                    { '_id': article['uuid'].replace('-', '') },
                    { '$set': article['bson'] },
                    upsert = True
                )

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


class SpreadArticleSanitizeTest(BaseSpreadTest):
    mocks_mask = set().union(BaseSpreadTest.mocks_mask)
    mocks = set().union(BaseSpreadTest.mocks)

    mocks.add('tornado')

    def mock_tornado(self):
        logger.info('STARTING: mock tornado')

        if 'tornado' in self.mocks_mask:
            logger.info('STOPPING: mock tornado—MASKED')

            return False

        _ = mock.patch(self.real_module + '.tornado.httpclient.HTTPClient')

        self.addCleanup(_.stop)

        mocked_httpclient_constructer = _.start()

        self.mocked_httpclient = mock.MagicMock()
        mocked_httpclient_constructer.return_value = self.mocked_httpclient

        self.mocked_response = mock.MagicMock()
        self.mocked_httpclient.fetch.return_value = self.mocked_response

        logger.info('STOPPING: mock tornado')

        return True

    def test_article_sanitize_parsed_not_modified(self):
        '''spread.articles—sanitize—not modified'''

        for article in self.articles['all']:
            article['bson']['original_etag'] = 'cee086c837e3a8f3496addee84a2e136'

            if self.mock_tornado():
                headers = {
                    'ETag': article['bson']['original_etag']
                }

                self.mocked_response.headers.__getitem__.side_effect = lambda _: headers[_]

                type(self.mocked_response).buffer = mock.PropertyMock(return_value = article['original_html'])

            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['parsed_at'],
                    article['bson']['updated_at'],
                ]

            is_datastore_mocked = self.mock_datastores()
            if is_datastore_mocked:
                self.mocked_collection.find_one.return_value = copy.deepcopy(article['bson'])

            sanitize_article({ 'uuid': article['message_body']['uuid'] }, self.mocked_message)

            if is_datastore_mocked:
                self.assertFalse(self.mocked_collection.update.called)

            self.mocked_message.ack.assert_called_once_with()

    def test_article_sanitize_unparsed(self):
        '''spread.articles—sanitize—not parsed

        identical cases:

        1. spread.articles—santiize—parsed,modified

        '''

        for article in self.articles['all']:
            original_etag = 'cee086c837e3a8f3496addee84a2e136'

            if self.mock_tornado():
                headers = {
                    'ETag': original_etag,
                }

                self.mocked_response.headers.__getitem__.side_effect = lambda _: headers[_]

                type(self.mocked_response).buffer = mock.PropertyMock(return_value = article['original_html'])

            if self.mock_datetime():
                self.mocked_datetime.now.side_effect = [
                    article['bson']['parsed_at'],
                    article['bson']['updated_at'],
                ]

            is_datastore_mocked = self.mock_datastores()
            if is_datastore_mocked:
                self.mocked_collection.find_one.return_value = copy.deepcopy(article['bson'])
                self.mocked_gridfs.put.return_value = article['bson']['body']

            sanitize_article({ 'uuid': article['message_body']['uuid'] }, self.mocked_message)

            del article['bson']['_id']
            article['bson']['original_etag'] = original_etag

            if is_datastore_mocked:
                self.mocked_collection.update.assert_called_once_with(
                    { '_id': article['uuid'].replace('-', '') },
                    { '$set': article['bson'] },
                    upsert = True
                )

            self.mocked_message.ack.assert_called_once_with()
