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

class UserCreationTest(unittest2.TestCase):
    def setUp(self):
        MARGARINE_API.config["TESTING"] = True
        self.application = MARGARINE_API.test_client()

        self.account_name = "test_user"

        self.url = "/{i.API_VERSION}/users/{username}"
        self.url = self.url.format(username = self.account_name, i = information)

        patcher = mock.patch("margarine.api.user.get_collection")
        mock_get_collection = patcher.start()

        self.addCleanup(patcher.stop)

        mock_get_collection.return_value = mock.MagickMock()

        patcher = mock.patch("margarine.api.user.get_channel")
        mock_get_channel = patcher.start()

        self.addCleanup(patcher.stop)

        mock_get_channel.return_value = mock.MagicMock()

    def test_user_creation_request(self):
        """Create a new (non-existent) user."""

        # TODO Mock user retrieval (non-existent user).

        response = self.application.put(self.url, data = {
            "email": "test@example.com",
            })

        self.assertIn("202", response.status)

        # Ensure publish has a routing_key parameter of users.create.

    def test_existing_user_read_request(self):
        """Read an existing user."""

        # TODO Mock user retrieval (existing user).

        response = self.application.get(self.url)

        self.assertIn("200", response.status)

    def test_nonexistent_user_read_request(self):
        """Read a non-existent user."""

        # TODO Mock user retrieval (non-existent user).

        resposne = self.application.get(self.url)

        self.assertIn("404", response.status)

    def test_user_update_request(self):
        """Update an existing user."""

        # TODO Mock user retrieval.

        response = self.application.put(self.url, data = {
            "email": "test@example.com",
            "name": "Test User",
            })

        self.assertIn("202", response.status)

        # Ensure publish has a routing_key parameter of users.update.

    def test_user_delete_request(self):
        """Delete an existing user."""

        # TODO Mock user retrieval.

        response = self.application.delete(self.url)

        self.assertIn("200", response.status)

        # And again to prove idempotency:

        response = self.application.delete(self.url)

        self.assertIn("200", response.status)

