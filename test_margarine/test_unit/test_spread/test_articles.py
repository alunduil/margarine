# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import mock
import logging
import uuid

from test_margarine.test_common import BaseMargarineTest

from margarine import queues
from margarine.spread.articles import create_article

logger = logging.getLogger(__name__)


class SpreadArticleCreateTest(BaseMargarineTest):
    mocks_mask = set()
    mocks = set()

    def setUp(self):
        super(SpreadArticleCreateTest, self).setUp()

        self.mocked_message = mock.MagicMock()

    mocks.add('datetime')

    def mock_datetime(self):
        logger.info('STARTING: mock datetime')

        if 'datetime' in self.mocks_mask:
            logger.info('STOPPING: mock datetime—MASKED')

            return False

        _ = mock.patch(self.real_module + '.datetime.datetime')

        self.addCleanup(_.stop)

        self.mocked_datetime = _.start()
        self.mocked_datetime.side_effect = lambda *args, **kwargs: datetime.datetime(*args, **kwargs)

        logger.info('STOPPING: mock datetime')

        return True

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
                    declare = [ queues.ARTICLES_FANOUT_EXCHANGE ]
                )

            self.mocked_message.ack.assert_called_once_with()

    def test_article_create_submitted(self):
        '''spread.articles—create—submitted'''

        for article in self.articles['all']:
            is_datastore_mocked = self.mock_datastores()
            if is_datastore_mocked:
                self.mocked_collection.find_one.return_value = article['bson']

            is_queue_mocked = self.mock_queues()

            create_article(article['message_body'], self.mocked_message)

            article['bson'].pop('body')
            article['bson'].pop('etag')
            article['bson'].pop('parsed_at')

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
                    declare = [ queues.ARTICLES_FANOUT_EXCHANGE ]
                )

            self.mocked_message.ack.assert_called_once_with()
