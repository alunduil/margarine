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

from margarine.aggregates import dirty
from margarine.aggregates import BaseAggregate

USER_SCHEMA_VERSION = 1

class User(BaseAggregate):
    def __init__(**kwargs):
        """Create a new user object from the properties passed.

        If no properties are passed, a blank initialized User object will be
        created.  If properties are passed, they will be used in the
        initialization of the object (thus tying this object to an existing
        data store item &c).

        Arguments
        ---------

        :kwargs: The generic keyword arguments handler so we can provide sane
                 defaults for derived or generated properties during creation.

                 The schema (the provided interface for this object) dictates
                 which parameters will be utilized by this initializer and may
                 change as the schema changes.

        These models have the concept of a dirty state which indicates that
        some or all properties need to be synced to the data store.  Because we
        are currently working against a document store we simply update the
        entire aggregate when the object goes out of scope or is explicitly
        saved (self.save).

        """

        super().__init__()

        self.uuid4 = uuid.uuid4() if "uuid4" not in kwargs else kwargs["uuid4"]

        self.username = kwargs["username"]

    @property
    def uuid(self):
        """UUID property of User.

        Currently, the UUID4 algorithm is in use but if the UUID5 algorithm
        adds an appropriate namespace, then UUID5 should be used instead.

        """

        pass

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


