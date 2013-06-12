# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest2

from margarine.consumers.users import create_user_consumer

class UserCreationTest(unittest2.TestCase):
    def setUp(self):
        patcher = mock.patch("margarine.consumers.get_channel")
        mock_get_channel = patcher.start()

        self.addCleanup(patcher.stop)

        mock_get_channel.return_value = mock.MagicMock()

        # TODO Mock the datastore insertion

        patcher = mock.patch("margarine.consumers.users.VERIFICATIONS")
        self.mock_verficiations = patcher.start()

        self.addCleanup(patcher.stop)

        # TODO Mock the email sender

    def test_user_creation_request(self):
        """Create a new (non-existent) user."""

        message = '{"username": "test_user", "password": null, "email": "test@example.com", "name": null}'

        create_user_consumer(None, None, None, message)

        self.mock_verifications.assert_called_once_with(mock.ANY, 'test_user')

