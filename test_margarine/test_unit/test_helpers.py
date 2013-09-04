# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest
import logging

from margarine.helpers import URI # TODO A better location for this URI parser?

logger = logging.getLogger(__name__)

# TODO powersets!  Using powersets we can reduce the number of cases created.
# TODO are powerserts desireable

class URITest(unittest.TestCase):
    def _verify_uri(self, uri, components = ()):
        '''Helper for verifying the given uri has the given components.

        Parameters
        ----------

        :``uri``: The string URI being verified
        :``components``: The broken component values as a tuple

        .. note::
            An empty components tuple will test no values and is useless.

        The components are assumed to be in order of the individual components
        that are parsed.  Missing items must be None.

        If the wrong number of components are passed the test will fail.

        '''

        _ = URI(uri)

        properties = [
                'scheme',
                'username',
                'password',
                'host',
                'port',
                'path', # TODO extend URI for query and anchor portions.
                ]

        if len(components) != len(properties):
            self.fail('{} URI components given; expected {}'.format(len(components), len(properties)))

        for _property, component in zip(properties, components):
            value = getattr(_, _property)

            if component is None:
                self.assertIsNone(value)
            else:
                self.assertEqual(component, value)

    def test_uri_components_0(self):
        '''URI—0 Components

        Verify the empty URI results in all None values.

        '''

        uris = {
                '': (None, None, None, None, None, None),
                }

        for uri, components in uris.iteritems():
            self._verify_uri(uri, components)

    def test_uri_components_1(self):
        '''URI—1 Components

        Verify a lonely hostname is parsed correctly.

        .. note::
            The only allowed single component URI is a hostname.

        '''

        uris = {
                'localhost': (None, None, None, 'localhost', None, None),
                }

        for uri, components in uris.iteritems():
            self._verify_uri(uri, components)

    def test_uri_components_2(self):
        '''URI—2 Components

        Verify a hostname and one other component.  We have choices for that
        other component unlike the previous test:

        * scheme
        * username
        * port
        * path

        All of these components with the required single component, hostname,
        will get us two components.

        '''

        uris = {
                'localhost:50': (None, None, None, 'localhost', '50', None),
                'localhost/example/index.html': (None, None, None, 'localhost', None, '/example/index.html'),
                'scheme://localhost': ('scheme', None, None, 'localhost', None, None),
                'user@localhost': (None, 'user', None, 'localhost', None, None),
                }

        for uri, components in uris.iteritems():
            self._verify_uri(uri, components)

    def test_uri_components_3(self):
        '''URI—3 Components

        Verify the three component URIs (all including hostname):

        * scheme, username
        * scheme, port
        * scheme, path
        * username, password
        * username, port
        * username, path
        * port, path

        '''

        uris = {
                'scheme://user@localhost': ('scheme', 'user', None, 'localhost', None, None),
                'scheme://localhost:50': ('scheme', None, None, 'localhost', '50', None),
                'scheme://localhost/example/index.html': ('scheme', None, None, 'localhost', None, '/example/index.html'),
                'user:pass@localhost': (None, 'user', 'pass', 'localhost', None, None),
                'user@localhost:50': (None, 'user', None, 'localhost', '50', None),
                'user@localhost/example/index.html': (None, 'user', None, 'localhost', None, '/example/index.html'),
                'localhost:50/example/index.html': (None, None, None, 'localhost', '50', '/example/index.html'),
                }

        for uri, components in uris.iteritems():
            self._verify_uri(uri, components)

    def test_uri_components_4(self):
        '''URI—4 Components

        Verify the four component URIs (all including hostname):

        * scheme, username, password
        * scheme, username, port
        * scheme, username, path
        * scheme, port, path
        * username, password, port
        * username, password, path
        * username, port, path

        '''

        uris = {
                'scheme://user:pass@localhost': ('scheme', 'user', 'pass', 'localhost', None, None),
                'scheme://user@localhost:50': ('scheme', 'user', None, 'localhost', '50', None),
                'scheme://user@localhost/example/index.html': ('scheme', 'user', None, 'localhost', None, '/example/index.html'),
                'scheme://localhost:50/example/index.html': ('scheme', None, None, 'localhost', '50', '/example/index.html'),
                'user:pass@localhost:50': (None, 'user', 'pass', 'localhost', '50', None),
                'user:pass@localhost/example/index.html': (None, 'user', 'pass', 'localhost', None, '/example/index.html'),
                'user@localhost:50/example/index.html': (None, 'user', None, 'localhost', '50', '/example/index.html'),
                }

        for uri, components in uris.iteritems():
            self._verify_uri(uri, components)

    def test_uri_components_5(self):
        '''URI—5 Components

        Verify the five component URIs (all including hostname):

        * scheme, username, password, port
        * scheme, username, password, path
        * scheme, username, port, path
        * username, password, port, path

        '''

        uris = {
                'scheme://user:pass@localhost:50': ('scheme', 'user', 'pass', 'localhost', '50', None),
                'scheme://user:pass@localhost/example/index.html': ('scheme', 'user', 'pass', 'localhost', None, '/example/index.html'),
                'scheme://user@localhost:50/example/index.html': ('scheme', 'user', None, 'localhost', '50', '/example/index.html'),
                'user:pass@localhost:50/example/index.html': (None, 'user', 'pass', 'localhost', '50', '/example/index.html'),
                }

        for uri, components in uris.iteritems():
            self._verify_uri(uri, components)

    def test_uri_components_6(self):
        '''URI—6 Components

        Verify the six component URIs (all including hostname):

        * scheme, username, password, port, path

        '''

        uris = {
                'scheme://user:pass@localhost:50/example/index.html': ('scheme', 'user', 'pass', 'localhost', '50', '/example/index.html'),
                }

        for uri, components in uris.iteritems():
            self._verify_uri(uri, components)
