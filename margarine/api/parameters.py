# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

from margarine.parameters import BASE_PARAMETERS

PARAMETERS = []

FLASK_PARAMETERS = [
        { # --host=HOST; HOST ← "127.0.0.1"
            "options": [ "--host" ],
            "default": "127.0.0.1",
            "help": "The IP to bind the API daemon; default: %(default)s.",
            },
        { # --port=PORT; PORT ← "5000"
            "options": [ "--port" ],
            "type": int,
            "default": 5000,
            "help": "The port to bind the API daemon; default: %(default)s.",
            },
        { # --debug
            "options": [ "--debug" ],
            "action": "store_true",
            "help": "Enable debugging of the flask application.",
            },
        ]

TOKEN_PARAMETERS = [
        { # --token-store-url=TOKEN_STORE_URL; TOKEN_STORE_URL ← "redis://localhost:6739"
            "options": [ "--token-store-url" ],
            "metavar": "TOKEN_STORE_URL",
            "default": "redis://localhost:6739",
            "help": "The token storage system to use; defaults: %(default)s.",
            },
        ]

PARAMETERS.extend(BASE_PARAMETERS)
PARAMETERS.extend(FLASK_PARAMETERS)
PARAMETERS.extend(TOKEN_PARAMETERS)

