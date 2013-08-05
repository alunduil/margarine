# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest
import mock

import logging
import uuid
import datetime

from test_margarine.test_unit.test_blend import BaseBlendTest

from margarine.blend import information
from margarine.blend import BLEND

logger = logging.getLogger(__name__)

class BaseBlendArticleTest(BaseBlendTest):
    def setUp(self):
        super(BaseBlendArticleTest, self).setUp()

        self.articles = [
                'http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html',
                'http://developer.rackspace.com/blog/got-python-questions.html',
                ]

        self.articles = dict([ (uuid.uuid5(uuid.NAMESPACE_DNS, _), _) for _ in self.articles ])

        self.base_url = '/{i.API_VERSION}/articles/'.format(i = information)

class BlendArticleCreateTest(BaseBlendArticleTest):
    def test_article_create(self):
        '''Article Create'''

        for uuid, url in self.articles.iteritems():
            response = self.application.post(self.base_url, data = {
                'url': url,
                })

            self.mock_channel.basic_publish.assert_called_once_with(
                    body = '{"url": "' + url + '", _id: "' + uuid.hex + '"}',
                    exchange = 'margarine.articles.topic',
                    properties = mock.ANY,
                    routing_key = 'articles.create'
                    )

            self.mock_channel.reset_mock()

            self.assertIn('202', response.status)

            self.assertEqual(url + str(uuid), response.headers.get('Location'))

class BlendArticleReadTest(BaseBlendArticleTest):
    def setUp(self):
        self.mock_mask = [
                'channel',
                'keyspace',
                ]

        super(BlendArticleReadTest, self).setUp()
        
    def test_article_read_unsubmitted(self):
        '''Article Read—Unsubmitted

        .. note::
            The article in question has not been submitted and thus nothing
            exists in the system for the requested article.

        '''

        self.mock_collection.find_one.return_value = None

        for uuid, url in self.articles.iteritems():
            response = self.application.get(self.base_url + str(uuid))

            self.assertIn('404', response.status)

    def test_article_read_submitted_incomplete(self):
        '''Article Read—Submitted,Incomplete

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

    def test_article_read_submitted_complete(self):
        '''Article Read—Submitted,Complete

        .. note::
            The article in question has been submitted and the spread process
            has finished processing the following items:

            * HTML Sanitization

        '''

        for uuid, url in self.articles.iteritems():
            self.mock_collection.find_one.return_value = {
                    '_id': uuid.hex,
                    'url': url,
                    'created_at': datetime.datetime(2013, 8, 4, 14, 16, 20, 77773),
                    'body': 'Redacted for testing purposes',
                    'etag': 'bf6285d832a356e1bf509a63edc8870f',
                    'parsed_at': datetime.datetime(2013, 8, 4, 14, 16, 21, 77773),
                    'size': 31052,
                    }

            response = self.application.get(self.base_url + str(uuid))

            self.mock_collection.assert_called_once_with({ '_id': uuid.hex })

            self.mock_collection.reset_mock()

            self.assertIn('200', response.status)

            self.assertEqual('application/json', response.headers.get('Content-Type'))
            # TODO Verify configured domain.
            self.assertEqual('http://margarine.raxsavvy.com', response.headers.get('Access-Control-Allow-Origin'))

class BlendArticleUpdateTest(BaseBlendArticleTest):
    def setUp(self):
        self.mock_mask = [
                'collection',
                'channel',
                'keyspace',
                ]

        super(BlendArticleUpdateTest, self).setUp()
        
    def test_article_update(self):
        '''Article Update'''

        for uuid, url in self.articles.iteritems():
            response = self.application.put(self.base_url + str(uuid))

            self.assertIn('405', response.status)

class BlendArticleDeleteTest(BaseBlendArticleTest):
    def setUp(self):
        self.mock_mask = [
                'collection',
                'channel',
                'keyspace',
                ]

        super(BlendArticleDeleteTest, self).setUp()
        
    def test_article_delete(self):
        '''Article Delete'''

        for uuid, url in self.articles.iteritems():
            response = self.application.delete(self.base_url + str(uuid))

            self.assertIn('405', response.status)

