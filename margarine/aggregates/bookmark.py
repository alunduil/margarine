# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""Interaction code for information about the Bookmark aggregate.

The properties we're starting with are the following:

    * uuid5 (url)
    * url
    * text → sent to object store upon save (MQ)
    * tags
    * notations

      * location
      * note

    * votes
    * created_at
    * original_etag
    * parsed_at
    
    * subscribers—Psuedo parameter, maps to join collection.

      * uuid4—user 
      * uuid5—bookmark
      * subscribed_at

"""

BOOKMARK_SCHEMA_VERSION = 1

class Bookmark(object):
    def __init__():
        pass

    @classmethod
    def find(cls, **kwargs):
        pass

    def save(self):
        pass

    @property
    def uuid5(self):
        pass

    @property
    def url(self):
        pass

    @property
    def text(self):
        pass

    @property
    def tags(self):
        return list(self.iter_tags())

    def iter_tags(self):
        pass

    @property
    def notations(self):
        return list(self.iter_notations())

    def iter_notations(self):
        pass

    @property
    def votes(self):
        pass

    @property
    def subscribers(self):
        return list(self.iter_subscribers())

    def iter_subscribers(self):
        pass

    @property
    def created_at(self):
        pass

    @property
    def original_etag(self):
        pass

    @property
    def parsed_at(self):
        pass

