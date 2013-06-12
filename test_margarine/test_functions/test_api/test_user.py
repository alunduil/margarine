# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest2
import logging

from margarine.api import information
from margarine.api import MARGARINE_API

logger = logging.getLogger(__name__)

class UserCreationTest(unittest2.TestCase):
    def setUp(self):
        MARGARINE_API.config["TESTING"] = True
        self.application = MARGARINE_API.test_client()
        self.account_name = "test_user"

        # TODO Mock the queue connection.

    def test_signup_request(self):
        url = "/{i.API_VERSION}/users/{username}"
        url = url.format(username = self.account_name, i = information)

        logger.debug("url: %s", url)
        
        response = self.application.put(url, data = {
            "email": "test@example.com",
            })

        logger.debug("response: %s", response)
        logger.debug("response.status: %s", response.status)
        logger.debug("response.__dict__: %s", response.__dict__.keys())
        logger.debug("response.data: %s", response.data)

        self.assertIn("202", response.status)

