# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from margarine.parameters import Parameters

Parameters('flask', parameters = [
    { # --flask-host=HOST; HOST ← 127.0.0.1
        'options': [ '--host' ],
        'default': '127.0.0.1',
        'help': \
                'The IP to bind the flask application.  This affects both ' \
                'tinge and blend and defaults to %(default)s.',
        },
    { # --flask-port=PORT; PORT ← 5050
        'options': [ '--port' ],
        'type': int,
        'default': 5050,
        'help': \
                'The port to bind the flask application.  This affects both ' \
                'tinge and blend and defaults to %(default)s.',
        },
    { # --flask-debug
        'options': [ '--debug' ],
        'action': 'store_true',
        'default': False,
        'help': \
                'Turn on flask application debugging.  This should never be ' \
                'enabled in production environments but can be used in ' \
                'development to assist in troubleshooting',
        },
    ])
