# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""Interaction code for information about the User aggregate.

The data schema we're starting with is simple and could potentially be moved
to a key-value datastore with pickling as a marshalling technique.

The properties we're starting with are the following:

    * uuid4 (uuid5 username namespace?)
    * username
    * email
    * name
    * password → md5(username:realm:password)

"""

USER_SCHEMA_VERSION = 1

class User(object):
    def __init__():
        pass

    @classmethod
    def find(cls, **kwargs):
        pass

    def save(self):
        pass

    @property
    def uuid4(self):
        pass

# TODO Switch to UUID5 with an appropriate namespace if one becomes available.
#    @property
#    def uuid5(self):
#        pass

    @property
    def username(self):
        pass

    @property
    def email(self):
        pass

    @property
    def name(self):
        pass

    @property
    def authentication_hash(self):
        pass

