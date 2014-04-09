# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import vagrant


class Box(object):
    def __init__(self, name):
        self.name = name
        self.vagrant = vagrant.Vagrant()

    @property
    def is_up(self):
        try:
            return self.vagrant.status(self.name).get(self.name, 'not_created') == 'running'
        except RuntimeError:
            return False

    def destroy(self):
        self.vagrant.destroy(vm_name = self.name)

    def up(self):
        self.vagrant.up(vm_name = self.name)
