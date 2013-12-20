# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import socket

from margarine.parameters import Parameters

Parameters('tinge', parameters = [
    { # --tinge-url=FQDN; FQDN ← HOSTNAME (TLD)
        'options': [ '--url' ],
        'default': 'http://' + '.'.join(socket.gethostname().rsplit('.', 2)[1:]),
        'help': \
                'The URL that tinge will be configured to run behind.  This ' \
                'is used to set the Access-Control-Allow-Origin header that ' \
                'lets browsers know that tinge on a different domain can ' \
                'use the data provided by blend.',
        },
    ])

# TODO Remove this alias with 2.x
Parameters('server', parameters = [
    { # --server-domain=FQDN; FQDN ← HOSTNAME (TLD)
        'options': [ '--domain' ],
        'default': 'http://' + '.'.join(socket.gethostname().rsplit('.', 2)[1:]),
        'help': \
                'The URL that tinge will be configured to run behind.  This ' \
                'is used to set the Access-Control-Allow-Origin header that ' \
                'lets browsers know that tinge, on a different domain, can ' \
                'use the data provided by blend.',
        },
    ])
