# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest2
import logging
import mock

from margarine.api import information
from margarine.api import MARGARINE_API

logger = logging.getLogger(__name__)

class BaseUserTest(unittest2.TestCase):
    def setUp(self):
        MARGARINE_API.config["TESTING"] = True
        self.application = MARGARINE_API.test_client()

        self.account_name = "test_user"

        self.url = "/{i.API_VERSION}/users/{username}"
        self.url = self.url.format(username = self.account_name, i = information)

    def get_mock_channel(self):
        """Setup and return a mock channel for further interaction.

        Return
        ------

        Mocked channel for faked queue interactions.

        """

        patcher = mock.patch("margarine.api.user.get_channel")
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

        patcher = mock.patch("margarine.api.user.get_collection")
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

        patcher = mock.patch("margarine.api.user.get_keyspace")
        mock_get_keyspace = patcher.start()

        self.addCleanup(patcher.stop)

        mock_keyspace = mock.MagicMock()
        mock_get_keyspace.return_value = mock_keyspace

        return mock_keyspace

class UserCreationTest(BaseUserTest):
    def setUp(self):
        super().setUp()

        self.mock_collection = self.get_mock_collection()
        self.mock_channel = self.get_mock_channel()

    def test_nonexistent_user_creation_request(self):
        """Create a new (non-existent) user."""

        self.mock_collection.find_one.return_value = None # TODO Verify this return value…

        response = self.application.put(self.url, data = {
            "email": "test@example.com",
            })

        self.assertIn("202", response.status)

        self.mock_channel.basic_publish.assert_called_once_with() # TODO Add parameters to assertion.

    def test_existing_user_creation_request(self):
        """Create an existing user."""

        self.mock_collection.find_one.return_value = {
                "_id": None,
                "username": self.account_name,
                "email": "test@example.com",
                }

        response = self.application.put(self.url, data = {
            "email": "test@example.com",
            })

        self.assertIn("401", response.status)

        self.assertFalse(self.mock_channel.basic_publish.called) 

class UserReadTest(BaseUserTest):
    def setUp(self):
        super(UserReadTest, self).setUp()

        self.mock_collection = self.get_mock_collection()

    def test_existing_user_read_request(self):
        """Read an existing user."""

        self.mock_collection.find_one.return_value = {
                "_id": None,
                "username": self.account_name,
                "email": "test@example.com",
                }

        response = self.application.get(self.url)

        self.assertIn("200", response.status)

    def test_nonexistent_user_read_request(self):
        """Read a non-existent user."""

        self.mock_collection.find_one.return_value = None # TODO Verify this return value.

        response = self.application.get(self.url)

        self.assertIn("404", response.status)

class UserUpdateTest(BaseUserTest):
    def setUp(self):
        super(UserUpdateTest, self).setUp()

        self.mock_collection = self.get_mock_collection()
        self.mock_keyspace = self.get_mock_keyspace()
        self.mock_channel = self.get_mock_channel()

    def test_user_update_request(self):
        """Update an existing user."""

        token = "c2d52150-08d1-4ae3-b19c-323c9e37813d"

        self.mock_keyspace.get.return_value = self.account_name

        response = self.application.put(self.url,
                headers = {
                    "X-Auth-Token": token,
                    },
                data = {
                    "email": "test@example.com",
                    "name": "Test User",
                    })

        self.mock_keyspace.get.assert_called_with(token)

        self.mock_channel.basic_publish.assert_called_once_with(
                body = '{"username": "test_user", "password": null, "email": "test@example.com", "name": "Test User"}',
                exchange = 'margarine.users.topic',
                properties = mock.ANY,
                routing_key = 'users.update'
                )

        self.assertIn("202", response.status)

class UserDeleteTest(BaseUserTest):
    def setUp(self):
        super(UserDeleteTest, self).setUp()

        self.mock_keyspace = self.get_mock_keyspace()
        self.mock_collection = self.get_mock_collection()

    def test_user_delete_request(self):
        """Delete an existing user."""

        token = "c2d52150-08d1-4ae3-b19c-323c9e37813d"

        self.mock_keyspace.get.return_value = self.account_name

        response = self.application.delete(self.url)

        self.mock_keyspace.get.assert_called_with(token)

        self.assertIn("200", response.status)

        # And again to prove idempotency:

        response = self.application.delete(self.url)

        self.assertIn("200", response.status)

    def test_unauthenticated_user_delete_request(self):
        """Delete an existing user without a proper token."""

        self.mock_keyspace.get.return_value = None

        response = self.application.delete(self.url)

        self.assertIn("401", response.status)

