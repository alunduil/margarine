# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from margarine.parameters import Parameters

Parameters('queue', parameters = [
    { # --queue-url=URL; URL ← amqp://guest:guest@localhost
        'options': [ '--url' ],
        'default': 'amqp://guest:guest@localhost',
        'help': \
                'The URL endpoint of the intra-service communication ' \
                'mechanism.  This can be a socket (the default) or an AMQP ' \
                'endpoint or anything between that\'s supported.',
        },
    { # --queue-wait=T; T ← 5
        'options': [ '--wait' ],
        'default': 5,
        'type': int,
        'help': \
                'The number of seconds to wait until attempting another ' \
                'connection to the queue server.  This application ' \
                'continually retries its connection every %(metavar)s ' \
                'seconds.',
        },
    ])
