# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

from margarine.parameters import CONFIGURATION_DIRECTORY

PARAMETERS = [
        { # --host=HOST, -h=HOST; HOST ← "127.0.0.1:5000"
            "options": [ "--host", "-h" ],
            "help": \
                    "The host to bind the API daemon to and the address " \
                    "plus port that will be listened on.",
            },
        ]

