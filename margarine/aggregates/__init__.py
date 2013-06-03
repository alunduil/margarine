# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import sys

from margarine.parameters import Parameters

Parameters("datastore", parameters = [
    { # --datastore-url=URL; URL ← "sqlite:///tmp/APP.sql
        "options": [ "--url" ],
        "default": "sqlite:///tmp/{0}.sqlite".format(sys.argv[0].rsplit('/', 1)[-1]),
        "help": \
                "The URL endpoint of the data store mechanism.  This can be " \
                "a local sqlite database but typically will be set to a " \
                "MongoDB instance.",
        }
    ])

class BaseAggregate(object):
    """Provide base implementations that are common to all aggregates.

    Common functionality for aggregates includes a basic find implementation, a
    concept of saving, &c.

    The entire purpose of this class is to keep margarine's aggregates as DRY
    as possible.

    .. note::
        MongoDB dcouments are limited to 16MB in size.

    """

    def __init__(self, *args, **kwargs):
        """Initialize the common components of Aggregates.

        Creates and initializes the _dirty property of the object.  Without
        this there is no auto-save feature of Aggregates.  This does need to be
        coupled with marking the setters as @dirty.

        """

        super(BaseAggregate, self).__init__(*args, **kwargs)

        super(BaseAggregate, self).__setattr__("autosave", True)
        super(BaseAggregate, self).__setattr__("_properties", {})

    def __del__(self):
        """Garbage collect an Aggregate.

        If the Aggregate is marked as dirty then it has not been saved and
        needs to be flushed to the data store.

        """

        if any([ dirty for _, dirty in self._properties.itervalues() ]) and self.autosave:
            self.save()

        super(BaseAggregate, self).__del__()

    def __getattr__(self, name):
        if name not in self._properties:
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, name))

        return self._properties[name][0]

    def __setattr__(self, name, value):
        """Set the specified property to the given value.

        The value is not only stored in our internal properties map but also
        marked dirty.  If the value is None, the item is instead removed from
        the properties as we don't store ø values in document stores.

        """

        if value is None and name in self._properties:
            del self._properties[name]
        else:
            self._properties[name] = [value, True]

    def __delattr__(self, name):
        del self._properties[name]

    def save(self):
        """Flush the Aggregate to the data store.

        Ensures that the Aggregrate is stored in the data store and an attempt
        will be made to call this when an object's reference count reaches
        zero.

        This also resets the dirty state of the object if called explicitly.

        """

        # TODO Save to data store.

        # Mark all items as not dirty.
        for item in self._properties.iteritems():
            item[-1] = False

    def delete(self):
        """Remove the aggregate from the data store.

        Ensures that the Aggregate is removed from the data store.

        A method should be determined to bypass the save on delete so this
        method does not leave empty documents in the collection.

        """

        self.autosave = False

        # TODO Remove the document from the collection.

    @classmethod
    def find(cls, *args, **kwargs):
        """Generic search for the Aggregate.

        Given the criteria in ``kwargs`` we should be able to find a particular
        object or a set of objects and return them.  This always returns a list
        of Aggregates and never a particular Aggregate.

        """

        return [] # TODO Create generic query interface to data store.

    @classmethod
    def find_one(cls, *args, **kwargs):
        """Generic search for the Aggregate that returns one result.

        Given the criteria in ``kwargs`` we should be able to find a particular
        object or set of objects and return them.  This always returns a list
        of Aggregates and never a particular Aggregate.

        The difference between this method and the ``find`` method is that if
        less then or more than one result is found the result is ``None``.

        """

        results = cls.find(*args, **kwargs)

        if len(results) != 1:
            return None

        return results[0] 

