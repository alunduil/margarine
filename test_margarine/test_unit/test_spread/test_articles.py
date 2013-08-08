# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import mock

import logging
import uuid
import json
import datetime

from test_margarine.test_unit.test_spread import BaseSpreadTest

# TODO Remove pluralization of articles
from margarine.spread.articles import create_article_consumer

logger = logging.getLogger(__name__)

class BaseSpreadArticleTest(BaseSpreadTest):
    def setUp(self):
        self.add_mock_to_mask('keyspace')

        super(BaseSpreadArticleTest, self).setUp()

        # TODO Merge with articles from test_blend.test_article?
        self.articles = [
                'http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html',
                'http://developer.rackspace.com/blog/got-python-questions.html',
                ]

        self.articles = [ { '_id': uuid.uuid5(uuid.NAMESPACE_URL, _).hex, 'url': _ } for _ in self.articles ]

class SpreadArticleCreate(BaseSpreadArticleTest):
    def test_article_create_unsubmitted(self):
        '''Spread::Article Create—Unsubmitted

        .. note::
            Tests first submission of the article (nothing stored yet).

        '''

        test_datetime = datetime.datetime(2013, 8, 7, 20, 25, 41, 596627)

        method = mock.MagicMock()
        method.delivery_tag.return_value = 'create'

        for article in self.articles:
            self.mock_collection.find_one.return_value = None

            with mock.patch('.'.join([
                self.__module__.replace('test_', '').replace('unit.', ''),
                'datetime',
                ])) as mock_datetime:

                mock_datetime.datetime.now.return_value = test_datetime

                create_article_consumer(mock.MagicMock(), method, None, json.dumps(article))

            _id = article.pop('_id')
            article['created_at'] = test_datetime

            self.mock_collection.find_one.assert_called_once_with({ '_id': _id })
            self.mock_collection.update.assert_called_once_with({ '_id': _id }, { '$set': article }, upsert = True)
            self.mock_collection.reset_mock()

            self.mock_channel.basic_publish.assert_called_once_with(
                    body = json.dumps({ '_id': _id }),
                    exchange = 'margarine.articles.create',
                    properties = mock.ANY,
                    routing_key = 'articles.create')
            self.mock_channel.reset_mock()
