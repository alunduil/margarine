# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

from margarine.parameters import BASE_PARAMETERS

PARAMETERS = [
        { # --host=HOST, -h=HOST; HOST ← "127.0.0.1"
            "options": [ "--host" ],
            "default": "127.0.0.1",
            "help": "The IP to bind the API daemon; default: %(default)s.",
            },
        { # --port=PORT, -p=PORT; PORT ← "5000"
            "options": [ "--port" ],
            "type": int,
            "default": 5000,
            "help": "The port to bind the API daemon; default: %(default)s.",
            },
        ]

PARAMETERS.extend(BASE_PARAMETERS)

