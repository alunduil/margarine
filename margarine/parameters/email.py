# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import socket

from margarine.parameters import PARAMETERS

PARAMETERS.add_parameter(
    group = 'email',
    options = [ '--url' ],
    default = 'smtp://localhost',
    help = \
        'URL of email relay server. Default %(default)s'
)

PARAMETERS.add_parameter(
    group = 'email',
    options = [ '--from' ],
    default = 'noreply@' + socket.gethostname(),
    help = \
        'Email address used as the FROM address on sent emails.  Default ' \
        '%(default)s'
)
