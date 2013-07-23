# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import re

logger = logging.getLogger(__name__)

class URI(object):
    def __init__(self, uri):
        """Initialize a self-parsing URI object.

        The object will decompose a URI like the following into its standard
        components:

          scheme://username:password@hostname:port/path

        """

        self.uri = uri

        match = re.match( \
                r'((?P<scheme>[^:]+)://)?' \
                r'((?P<username>[^:]+)(:(?P<password>[^@]+))?@)?' \
                r'(?P<host>[^:/]+)?' \
                r'(:(?P<port>[^/]+))?' \
                r'(?P<path>/\w+)?' \
                , self.uri)

        self.scheme = match.group("scheme")
        self.username = match.group("username")
        self.password = match.group("password")
        self.host = match.group("host")
        self.port = match.group("port")
        self.path = match.group("path")

