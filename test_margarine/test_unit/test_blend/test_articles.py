# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import datetime
import json
import logging
import mock
import uuid
import unittest

from test_margarine.test_fixtures.test_articles import ARTICLES
from test_margarine.test_unit.test_blend import BaseBlendTest

from margarine.blend import BLEND
from margarine.blend import information

logger = logging.getLogger(__name__)


class BlendArticleReadTest(unittest.TestCase):
    mocks_mask = set()
    mocks = set()

    def setUp(self):
        super(BlendArticleReadTest, self).setUp()

        articles_copy = copy.copy(ARTICLES)
        def _():
            ARTICLES = articles_copy
        self.addCleanup(_)

        BLEND.config['TESTING'] = True
        self.application = BLEND.test_client()

        self.base_url = '/{i.API_VERSION}/articles/'.format(i = information)

    mocks.add('datastores.get_collection')
    def mock_datastore(self, **kwargs):
        if 'datastores.get_collection' in self.mocks_mask:
            return

        _ = mock.patch('margarine.blend.articles.get_collection')

        self.addCleanup(_.stop)

        self.mocked_datastore = _.start()

        self.mocked_collection = mock.MagicMock()
        self.mocked_datastore.return_value = self.mocked_collection

        for function, value in kwargs.iteritems():
            logger.debug('function: %s', function)
            logger.debug('value: %s', value)

            getattr(self.mocked_collection, function).return_value = value

    mocks.add('datastores.get_container')
    def mock_pyrax(self, contents):
        if 'datastores.get_container' in self.mocks_mask:
            return

        _ = mock.patch('margarine.blend.articles.get_container')

        self.addCleanup(_.stop)

        self.mocked_pyrax = _.start()

        self.mocked_container = mock.MagicMock()
        self.mocked_pyrax.return_value = self.mocked_container

        self.mocked_object = mock.MagicMock()
        self.mocked_container.get_object.return_value = self.mocked_object

        self.mocked_object.fetch.return_value = contents

    def test_article_read_unsubmitted(self):
        '''blend.articles—GET /articles/? → 404—unsubmitted'''

        self.mock_datastore()

        for article in ARTICLES['all']:
            response = self.application.get(self.base_url + article['uuid'])
            self.assertEqual(404, response.status_code)

    def test_article_read_submitted_incomplete(self):
        '''blend.articles-GET /articles/? → 404-submitted,incomplete'''
    
        for article in ARTICLES['all']:
            del article['bson']['parsed_at']
            self.mock_datastore(find_one = article['bson'])

            response = self.application.get(self.base_url + article['uuid'])

            self.assertEqual(404, response.status_code)

    def test_article_read_submitted(self):
        '''blend.articles—GET /articles/? → 200—submitted

        submitted means that all background processes have finished and all data
        is available in the datastore query result.

        '''

        for article in ARTICLES['all']:
            self.mock_datastore(find_one = article['bson'])
            self.mock_pyrax(article['json']['body'])

            response = self.application.get(self.base_url + article['uuid'])
            self.assertEqual(200, response.status_code)

            self.assertIsNotNone(response.headers.get('Access-Control-Allow-Origin'))

            self.assertEqual('application/json', response.headers.get('Content-Type'))

            self.assertEqual(article['etag'], response.headers.get('ETag'))
            self.assertEqual(article['updated_at'], response.headers.get('Last-Modified'))
            self.assertEqual('<{0}>; rel="original"'.format(article['url']), response.headers.get('Link'))

            _, self.maxDiff = self.maxDiff, None
            self.assertEqual(article['json'], json.loads(response.get_data()))
            self.maxDiff = _

class BaseBlendArticleTest(BaseBlendTest):
    # TODO Make this simpler.
    mock_mask = BaseBlendTest.mock_mask | set(['keyspace'])

    def setUp(self):
        super(BaseBlendArticleTest, self).setUp()

        self.articles = [
                'http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html',
                'http://developer.rackspace.com/blog/got-python-questions.html',
                ]

        self.articles = dict([ (uuid.uuid5(uuid.NAMESPACE_URL, _), _) for _ in self.articles ])

        self.base_url = '/{i.API_VERSION}/articles/'.format(i = information)

class BlendArticleCreateTest(BaseBlendArticleTest):
    def test_article_create(self):
        '''Blend::Article Create'''

        for uuid, url in self.articles.iteritems():
            response = self.application.post(self.base_url, data = {
                'url': url,
                })

            self.mock_channel.basic_publish.assert_called_once_with(
                    body = '{"url": "' + url + '", "_id": "' + uuid.hex + '"}',
                    exchange = 'margarine.articles.topic',
                    properties = mock.ANY,
                    routing_key = 'articles.create'
                    )

            self.mock_channel.reset_mock()

            self.assertIn('202', response.status)

            self.assertIn(self.base_url + str(uuid), response.headers.get('Location'))

class BlendArticleLegacyReadTest(BaseBlendArticleTest):
    # TODO Make this simpler.
    mock_mask = BaseBlendArticleTest.mock_mask | set(['channel'])

    def test_article_read_submitted_incomplete(self):
        '''Blend::Article Read—Submitted,Incomplete

        .. note::
            The article in question has been submitted but the spread process
            has not populated any information beyond the first consumption.

            * created_at

        '''

        for uuid, url in self.articles.iteritems():
            self.mock_collection.find_one.return_value = {
                    '_id': uuid.hex,
                    'url': url,
                    'created_at': datetime.datetime(2013, 8, 4, 14, 4, 12, 639560),
                    }

            response = self.application.get(self.base_url + str(uuid))

            self.mock_collection.find_one.assert_called_once_with({ '_id': uuid.hex })

            self.mock_collection.reset_mock()

            self.assertIn('404', response.status)

class BlendArticleUpdateTest(BaseBlendArticleTest):
    # TODO Make this simpler.
    mock_mask = BaseBlendArticleTest.mock_mask | set([
        'collection',
        'channel',
        ])

    def test_article_update(self):
        '''Blend::Article Update'''

        for uuid, url in self.articles.iteritems():
            response = self.application.put(self.base_url + str(uuid))

            self.assertIn('405', response.status)

class BlendArticleDeleteTest(BaseBlendArticleTest):
    # TODO Make this simpler.
    mock_mask = BaseBlendArticleTest.mock_mask | set([
        'collection',
        'channel',
        ])

    def test_article_delete(self):
        '''Blend::Article Delete'''

        for uuid, url in self.articles.iteritems():
            response = self.application.delete(self.base_url + str(uuid))

            self.assertIn('405', response.status)
