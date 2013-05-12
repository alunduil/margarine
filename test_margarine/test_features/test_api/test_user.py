# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import lettuce

@lettuce.step(r"I have a username, (\w+)")
def have_username(self, username):
    lettuce.world.usernaem = username

