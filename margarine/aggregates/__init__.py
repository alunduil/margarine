# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# TODO Think of a good synonym for dirty (verb).
def dirty(decorated):
    """Decorate the function with logic to mark the object dirty.

    Arguments
    ---------

    :decorated: The function we are wrapping.

    """

    def internal(self, *args, **kwargs):
        self._dirty = True

        return decorated(self, *args, **kwargs)

    internal.__name__ = decorated.__name__
    internal.__doc__ = decorated.__doc__
    internal.__dict__.update(decorated.__dict__)

    return internal

class BaseAggregate(object):
    """Provide base implementations that are common to all aggregates.

    Common functionality for aggregates includes a basic find implementation, a
    concept of saving, &c.

    The entire purpose of this class is to keep margarine's aggregates as DRY
    as possible.

    """

    def __init__(self, *args, **kwargs):
        """Initialize the common components of Aggregates.

        Creates and initializes the _dirty property of the object.  Without
        this there is no auto-save feature of Aggregates.  This does need to be
        coupled with marking the setters as @dirty.

        """

        super().__init__(self, *args, **kwargs)

        self._dirty = False

    def __del__(self, *args, **kwargs):
        """Garbage collect an Aggregate.

        If the Aggregate is marked as dirty then it has not been saved and
        needs to be flushed to the data store.

        """

        if self._dirty:
            self.save()

        super().__del__(self, *args, **kwargs)

    @classmethod
    def find(cls, *args, **kwargs):
        """Generic search for the Aggregate.

        Given the criteria in ``kwargs`` we should be able to find a particular
        object or a set of objects and return them.  This always returns a list
        of Aggregates and never a particular Aggregate.

        """

        pass # TODO Create generic query interface to data store.

    def save(self):
        """Flush the Aggregate to the data store.

        Ensures that the Aggregrate is stored in the data store and an attempt
        will be made to call this when an object's reference count reaches
        zero.

        This also resets the dirty state of the object if called explicitly.

        """

        # TODO Save to data store.

        self._dirty = False

