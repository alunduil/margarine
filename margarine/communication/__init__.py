# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from margarine.parameters import CONFIGURATION_FILE

class Queue(object):
    def __init__(self, queue_url = None):
        """Create a connection with the specified queue.

        Using the passed queue_url we should be able to decompose it into the
        following pieces of information:

        :protocol: Which queue protocol to use.  If this matches the registered
                   name of a backend plugin that backend plugin will be used to
                   provide the interface to the queue.
        :username: The username to login to the queue if required.
        :password: The password to login to the queue if required.
        :hostname: The hostname at which the queue is hosted.
        :port:     The port number at which the data store is hosted.

        The above pieces are put together in typical URL fashion:

        ::

            protocol://username:password@hostname:port

        """

        pass

    def qsize(self):
        pass

    def empty(self):
        pass

    def full(self):
        pass

    def put(self, item, block = True, timeout = None):
        pass

    def put_nowait(self, item):
        return self.put(item, False)

    def get(self, block = True, timeout = None):
        pass

    def get_nowait(self):
        return self.get(False)

    def task_done(self):
        pass

    def join(self):
        pass

