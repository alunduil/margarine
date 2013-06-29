# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest2
import logging
import mock
import uuid

from margarine.api import information
from margarine.api import MARGARINE_API

logger = logging.getLogger(__name__)

class BaseArticleTest(unittest2.TestCase):
    def setUp(self):
        MARGARINE_API.config["TESTING"] = True
        self.application = MARGARINE_API.test_client()

        self.article_url = "http://blog.alunduil.com/posts/an-explanation-of-lvm-snapshots.html"
        self.article_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, self.article_url)

        self.url = "/{i.API_VERSION}/articles/"
        self.url = self.url.format(i = information)

    def get_mock_channel(self):
        """Setup and return a mock channel for further interaction.

        Return
        ------

        Mocked channel for faked queue interactions.

        """

        patcher = mock.patch("margarine.api.article.get_channel")
        mock_get_channel = patcher.start()

        self.addCleanup(patcher.stop)

        mock_channel = mock.MagicMock()
        mock_get_channel.return_value = mock_channel

        return mock_channel

    def get_mock_collection(self):
        """Setup and return a mock collection for further interaction.

        Return
        ------

        Mocked collection for faked Mongo interactions.

        """

        patcher = mock.patch("margarine.api.article.get_collection")
        mock_get_collection = patcher.start()

        self.addCleanup(patcher.stop)

        mock_collection = mock.MagicMock()
        mock_get_collection.return_value = mock_collection

        return mock_collection

    def get_mock_keyspace(self):
        """Setup and return a mock keyspace for further interaction.

        Return
        ------

        Mocked keyspace for faked Redis interactions.

        """

        patcher = mock.patch("margarine.api.article.get_keyspace")
        mock_get_keyspace = patcher.start()

        self.addCleanup(patcher.stop)

        mock_keyspace = mock.MagicMock()
        mock_get_keyspace.return_value = mock_keyspace

        return mock_keyspace

class ArticleCreationTest(BaseArticleTest):
    def setUp(self):
        super(ArticleCreationTest, self).setUp()

        self.mock_channel = self.get_mock_channel()

    def test_article_creation_request(self):
        """Create Article."""

        response = self.application.post(self.url, data = {
            "url": self.article_url,
            })

        self.mock_channel.basic_publish.assert_called_once_with(
                body = '{"url": "' + self.article_url + '", _id: "' + self.article_uuid + '"}',
                exchange = 'margarine.articles.topic',
                properties = mock.ANY,
                routing_key = 'articles.create'
                )

        self.assertIn("202", response.status)
        self.assertIn("Location", response.headers)
        self.assertEqual(self.url + self.article_uuid, response.headers["Location"])

class ArticleReadTest(BaseArticleTest):
    def setUp(self):
        super(ArticleReadTest, self).setUp()

        self.mock_collection = self.get_mock_collection()

    def test_existing_article_get_request(self):
        """Read Article—Existing (GET)."""

        body = "" # TODO Lorem ipsum?

        self.mock_collection.find_one.return_value = {
                "_id": self.article_uuid,
                "url": self.article_url,
                }

        # TODO Mock the object store access with the body.

        response = self.application.get(self.url + self.article_uuid)

        self.assertIn("200", response.status)

        self.assertEqual(body, response.body)

    def test_existing_article_head_request(self):
        """Read Article-Existing (HEAD)."""

        self.mock_collection.find_one.return_value = {
                "sanitized_url": None, # TODO Change to proper URL.
                }

        # TODO Ensure that the object store is not called.

        response = self.application.head(self.url + self.article_uuid)

        self.mock_collection.find_one.assert_called_once_with(mock.ANY, {"sanitized_url": -1})

        self.assertIn("200", response.status)

        self.assertFalse(len(response.body))

    def test_nonexistent_article_get_request(self):
        """read article—not existing (get)."""

        self.mock_collection.find_one.return_value = None # todo verify this return value.

        response = self.application.get(self.url + self.article_uuid)

        self.assertin("404", response.status)

    def test_nonexistent_article_head_request(self):
        """read article—not existing (head)."""

        self.mock_collection.find_one.return_value = None # todo verify this return value.

        logger.debug("self.url: %s", self.url)

        response = self.application.head(self.url + str(self.article_uuid))

        self.assertin("404", response.status)

# No Updates on Articles Allowed!

class ArticleUpdateTest(BaseArticleTest):
    def test_article_update_existing_request(self):
        """Update Article—Existing."""

        response = self.application.put(self.url + str(self.article_uuid))

        self.assertIn("405", response.status)

    def test_article_update_nonexistent_request(self):
        """Update Article—Not Existing."""

        response = self.application.put(self.url + str(self.article_uuid))

        self.assertIn("405", response.status)

# No Deletes on Articles Allowed!

class ArticleDeleteTest(BaseArticleTest):
    def test_article_delete_request(self):
        """Delete Article—Existing."""

        response = self.application.delete(self.url + self.article_uuid)

        self.assertIn("405", response.status)

