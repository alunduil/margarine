# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import nose
import lettuce.bin
import os

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    lettuce.bin.main()

    nose.main()

