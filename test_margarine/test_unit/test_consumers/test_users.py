# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest2
import mock
import json

from margarine.consumers.users import create_user_consumer

class UserCreationTest(unittest2.TestCase):
    def setUp(self):
        patcher = mock.patch("margarine.consumers.users.get_collection")
        mock_get_channel = patcher.start()

        self.addCleanup(patcher.stop)

        self.mock_channel = mock.MagicMock()
        mock_get_channel.return_value = self.mock_channel

        patcher = mock.patch("margarine.consumers.users.get_keyspace")
        mock_get_keyspace = patcher.start()

        self.addCleanup(patcher.stop)

        self.mock_keyspace = mock.MagicMock()
        mock_get_keyspace.return_value = self.mock_keyspace

        patcher = mock.patch("margarine.consumers.users.send_user_email")
        self.mock_send_email = patcher.start()

        self.addCleanup(patcher.stop)

        self.password = "423jklfds78"

    def test_user_creation(self):
        """Create a new (non-existent) user not specifying password."""

        message = '{"username": "test_user", "email": "test@example.com", "name": null}'

        method = mock.MagicMock()
        method.delivery_tag.return_value = "create"

        # create_user_consumer(channel, method, header, body)
        create_user_consumer(mock.MagicMock(), method, None, message)

        self.mock_channel.insert.assert_called_once_with(json.loads(message))

        self.mock_keyspace.setex.assert_called_once_with(mock.ANY, "test_user", mock.ANY)

        self.mock_send_email.assert_called_once_with("create", user, self.password)

