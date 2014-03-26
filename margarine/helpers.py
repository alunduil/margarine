# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import re

logger = logging.getLogger(__name__)


class URI(object):
    '''A URI with accessible components.

    Breaks a URI string (passed into the constructor) into it's components and
    makes those components available as settable properties.

    This URI also has a proper string representation that rebuilds the original
    URI or modified URI.

    Examples
    --------

    >>> str(URI('scheme://username:password@hostname:port/path'))
    'scheme://username:password@hostname:port/path'

    >>> URI('scheme://username:password@hostname:port/path').host
    'hostname'

    '''

    def __init__(self, uri):
        self.uri = uri

        match = re.match(
            r'((?P<scheme>[^:]+)://)?'
            r'((?P<username>[^:]+)(:(?P<password>[^@]+))?@)?'
            r'(?P<host>[^:/]+)?'
            r'(:(?P<port>[^/]+))?'
            r'(?P<path>/[^\?]+)?',
            self.uri
        )

        self.scheme = match.group("scheme")
        self.username = match.group("username")
        self.password = match.group("password")
        self.host = match.group("host")
        self.port = match.group("port")
        self.path = match.group("path")

    def __str__(self):
        _ = ''

        if self.scheme is not None:
            _ += self.scheme + '://'

        if self.username is not None:
            _ += self.username

            if self.password is not None:
                _ += ':' + self.password

            _ += '@'

        if self.host is not None:
            _ += self.host

        if self.port is not None:
            _ += ':' + self.port

        if self.path is not None:
            _ += self.path

        return _
