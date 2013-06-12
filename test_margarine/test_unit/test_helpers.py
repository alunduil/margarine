# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest2

from margarine.helpers import URI

class URIParsingTest(unittest2.TestCase):
    def test_minimal_uri(self):
        uri = URI("")

        self.assertIsNone(uri.scheme)
        self.assertIsNone(uri.path)
        self.assertIsNone(uri.params)
        self.assertIsNone(uri.query)
        self.assertIsNone(uri.fragment)
        self.assertIsNone(uri.username)
        self.assertIsNone(uri.password)
        self.assertIsNone(uri.host)
        self.assertIsNone(uri.port)

    def test_host_only(self):
        uri = URI("hostname")

        self.assertIsNone(uri.scheme)
        self.assertIsNone(uri.path)
        self.assertIsNone(uri.params)
        self.assertIsNone(uri.query)
        self.assertIsNone(uri.fragment)
        self.assertIsNone(uri.username)
        self.assertIsNone(uri.password)
        self.assertEqual(uri.host, "hostname")
        self.assertIsNone(uri.port)

    def test_localhost_uri(self):
        uri = URI("scheme://localhost")

        self.assertEqual(uri.scheme, "scheme")
        self.assertIsNone(uri.path)
        self.assertIsNone(uri.params)
        self.assertIsNone(uri.query)
        self.assertIsNone(uri.fragment)
        self.assertIsNone(uri.username)
        self.assertIsNone(uri.password)
        self.assertEqual(uri.host, "localhost")
        self.assertIsNone(uri.port)

    def test_amqp_uri(self):
        uri = URI("amqp://rabbit:3bbd445d@example.com:8000/vhost1")

        self.assertEqual(uri.scheme, "amqp")
        self.assertEqual(uri.path, "/vhost1")
        self.assertIsNone(uri.params)
        self.assertIsNone(uri.query)
        self.assertIsNone(uri.fragment)
        self.assertEqual(uri.username, "rabbit")
        self.assertEqual(uri.password, "3bbd445")
        self.assertEqual(uri.host, "example.com")
        self.assertEqual(uri.port, "8000")

