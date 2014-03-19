# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import socket

from margarine.parameters import PARAMETERS

PARAMETERS.add_parameter(
    group = 'blend',
    options = [ '--url' ],
    default = 'http://api.' + '.'.join(socket.gethostname().rsplit('.', 2)[1:]),
    help = 'URL that is used as the endpoint for blend.  Default %(default)s.'
)
