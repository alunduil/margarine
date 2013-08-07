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

        self.mock_channel.find_one.return_value = None

        method = mock.MagicMock()
        method.delivery_tag.return_value = 'create'

        for article in self.articles:
            create_article_consumer(mock.MagicMock(), method, None, json.dumps(article))

            _id = article.pop('_id')

            self.mock_channel.find_one.assert_called_once_with({ '_id': _id })
            self.mock_channel.update.assert_called_once_with({ '_id': _id }, { '$set': article }, upsert = True)
            self.mock_channel.reset_mock()

            self.mock_channel.basic_publish.assert_called_once_with(
                    body = json.dumps({ '_id': _id }),
                    exchange = 'margarine.articles.create',
                    properties = mock.ANY,
                    routing_key = 'articles.create')
            self.mock_channel.reset_mock()
