# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import socket

from margarine.parameters import Parameters

Parameters('blend', parameters = [
    { # --tinge-url=FQDN; FQDN ← HOSTNAME (TLD)
        'options': [ '--url' ],
        'default': 'http://api.' + '.'.join(socket.gethostname().rsplit('.', 2)[1:]),
        'help': \
                'The URL that blend will be configured to run behind.  This ' \
                'is used to set up tinge\'s links to blend.',
        },
    ])

Parameters('api', parameters = [
    { # --api-endpoint=FQDN; FQDN ← HOSTNAME (TLD)
        'options': [ '--endpoint' ],
        'default': 'http://api.' + '.'.join(socket.gethostname().split('.', 2)[1:]),
        'help': \
                'The URL that blend will be configured to run behind.  This ' \
                'is used to set up tinge\'s links to blend.',
        },
    ])
