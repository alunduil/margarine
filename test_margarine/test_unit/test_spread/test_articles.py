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
    # TODO Make this simpler.
    mock_mask = BaseSpreadTest.mock_mask | set(['keyspace'])

    def setUp(self):
        super(BaseSpreadArticleTest, self).setUp()

        # TODO Merge with articles from test_blend.test_article?
        self.articles = [
                'http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html',
                'http://developer.rackspace.com/blog/got-python-questions.html',
                ]

        self.articles = [ { '_id': uuid.uuid5(uuid.NAMESPACE_URL, _).hex, 'url': _ } for _ in self.articles ]

        self.method = mock.MagicMock()

        self.test_datetime = datetime.datetime(2013, 8, 7, 20, 25, 41, 596627)

class SpreadArticleCreate(BaseSpreadArticleTest):
    def setUp(self):
        super(SpreadArticleCreate, self).setUp()

        self.method.delivery_tag.return_value = 'create'

    def _validate_mocks(self, _id, article):
        '''Validate mock calls.

        A simple helper method to reduce code duplication in these tests.

        '''

        self.mock_collection.find_one.assert_called_once_with({ '_id': _id })
        self.mock_collection.update.assert_called_once_with({ '_id': _id }, { '$set': article }, upsert = True)
        self.mock_collection.reset_mock()

        self.mock_channel.basic_publish.assert_called_once_with(
                body = json.dumps({ '_id': _id }),
                exchange = 'margarine.articles.create',
                properties = mock.ANY,
                routing_key = 'articles.create')
        self.mock_channel.reset_mock()

    def test_article_create_unsubmitted(self):
        '''Spread::Article Create—Unsubmitted

        .. note::
            Tests first submission of the article (nothing stored yet).

        '''

        for article in self.articles:
            self.mock_collection.find_one.return_value = None

            with mock.patch('.'.join([
                self.__module__.replace('test_', '').replace('unit.', ''),
                'datetime',
                ])) as mock_datetime:

                mock_datetime.datetime.now.return_value = self.test_datetime

                create_article_consumer(mock.MagicMock(), self.method, None, json.dumps(article))

            _id = article.pop('_id')
            article['created_at'] = self.test_datetime

            self._validate_mocks(_id, article)

    def test_article_create_submitted_incomplete(self):
        '''Spread::Article Create—Submitted,Incomplete

        .. note::
            The article has been submitted but only the top portion of the
            bottom half (consumer) has been run.

        Complete Actions
        ----------------

        * create_article_consumer

        Incopmlete Actions
        ------------------

        * update_references_consumer
        * sanitize_html_consumer

        '''

        for article in self.articles:
            self.mock_collection.find_one.return_value = article
            self.mock_collection.find_one.return_value['created_at'] = self.test_datetime

            create_article_consumer(mock.MagicMock(), self.method, None, json.dumps(article))

            _id = article.pop('_id')

            self._validate_mocks(_id, article)

    def test_article_create_submitted_incomplete_references(self):
        '''Spread::Article Create—Submitted,Incomplete - References

        .. note::
            The article has been submitted but only a portion of the bottom
            half (consumer) has been run.

        Complete Actions
        ----------------

        * create_article_consumer
        * update_references_consumer

        Incomplete Actions
        ------------------

        * sanitize_html_consumer

        '''

        self.fail('Implement this stub!')

    def test_article_create_submitted_incomplete_sanitization(self):
        '''Spread::Article Create—Submitted,Incomplete - Sanitization

        .. note::
            The article has been submitted but only a portion of the bottom
            half (consumer) has been run.

        Complete Actions
        ----------------

        * create_article_consumer
        * sanitize_html_consumer

        Incomplete Actions
        ------------------

        * update_references_consumer

        '''

        for article in self.articles:
            self.mock_collection.find_one.return_value = article

            self.mock_collection.find_one.return_value.update({
                'created_at': self.test_datetime,
                'etag': 'bf6285d832a356e1bf509a63edc8870f',
                'parsed_at': self.test_datetime,
                'size': 31052,

                # TODO Move this to a better datastore?
                'text_container_name': '44d85795',
                'text_object_name': '248d-5899-b8ca-ac2bd8233755',
                })

            create_article_consumer(mock.MagicMock(), self.method, None, json.dumps(article))

            _id = article.pop('_id')

            self._validate_mocks(_id, article)

    def test_article_create_submitted_complete(self):
        '''Spread::Article Create—Submitted,Complete

        .. note::
            The article is being resubmitted after all components have run.

        .. note::
            Until there are more functions implemented, this test is equivalent
            to test_article_create_submitted_incomplete_sanitization and is
            only a stub.

        '''

        self.fail('Implement this stub!')

class SpreadArticleReferencesTest(BaseSpreadArticleTest):
    def setUp(self):
        super(SpreadArticleReferencesTest, self).setUp()

        self.method.delivery_tag.return_value = 'references'

    def test_article_references(self):
        '''Spread::Article References'''

        self.fail('Implement this stub!')

class SpreadArticleSanitizationTest(BaseSpreadArticleTest):
    def setUp(self):
        super(SpreadArticleSanitizationTest, self).setUp()

        self.method.delivery_tag.return_value = 'sanitize'

    def test_article_sanitize(self):
        '''Spread::Article Sanitize'''

        self.fail('Implement this stub! Refactor sanitization.')
