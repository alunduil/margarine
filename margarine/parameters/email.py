# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import socket

from margarine.parameters import Parameters

Parameters('email', parameters = [
    { # --email-url=URL; URL ← smtp://localhost
        'options': [ '--url' ],
        'default': 'smtp://localhost',
        'help': \
                'The URL endpoint of the email relay server used by ' \
                'margarine ',
        },
    { # --email-from=EMAIL; EMAIL ← noreply@HOSTNAME
        'options': [ '--from' ],
        'default': 'noreply@' + socket.gethostname(), # TODO Parameters()["server.name"],
        'help': \
                'The email address used as the FROM address on all ' \
                'generated emails.',
        },
    ])
