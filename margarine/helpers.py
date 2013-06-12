# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import urlparse
import logging

logger = logging.getLogger(__name__)

class URI(object):
    def __init__(self, uri):
        """Initialize a self-parsing URI object.

        The object will decompose a URI like the following into its standard
        components:

          scheme://username:password@hostname:port/path;params?query#fragment

        """

        self.uri = uri

        _ = urlparse.urlparse(self.uri)

        self.scheme = _.scheme if len(_.scheme) else None
        self.path = _.path if len(_.path) else None
        self.params = _.params if len(_.params) else None
        self.query = _.query if len(_.query) else None
        self.fragment = _.fragment if len(_.fragment) else None

        logger.debug("Net Location: %s", _)

        _ = _.netloc.rsplit('@', 1)

        logger.debug("Split Net Location: %s", _)

        self.username, self.password = _[0].split(':', 1)

        self.host, self.port = _[1].rsplit(':', 1)

