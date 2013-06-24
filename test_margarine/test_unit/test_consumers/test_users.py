# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest2
import mock

from margarine.consumers.users import create_user_consumer

class UserCreationTest(unittest2.TestCase):
    def setUp(self):
        # TODO Mock the datastore insertion

        patcher = mock.patch("margarine.consumers.users.get_keyspace")
        mock_get_keyspace = patcher.start()

        self.addCleanup(patcher.stop)

        mock_get_keyspace.return_value = mock.MagicMock()

        # TODO Mock the email sender

    def test_user_creation_request(self):
        """Create a new (non-existent) user."""

        message = '{"username": "test_user", "password": null, "email": "test@example.com", "name": null}'

        method = mock.MagicMock()
        method.delivery_tag.return_value = "create"

        # create_user_consumer(channel, method, header, body)
        create_user_consumer(mock.MagicMock(), method, None, message)

        # TODO Verify the data store insertion.

        # TODO Verify the email sender.

