# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from margarine.parameters import PARAMETERS

PARAMETERS.add_parameter(
    group = 'flask',
    options = [ '--host' ],
    default = '127.0.0.1',
    help = \
        'IP to which flask should be bound.  Default %(default)s.'
)

PARAMETERS.add_parameter(
    group = 'flask',
    options = [ '--port' ],
    default = 5000,
    type = int,
    help = \
        'Port to which flask should be bound.  Default $(default)s.'
)

PARAMETERS.add_parameter(
    group = 'flask',
    options = [ '--debug' ],
    action = 'store_true',
    default = False,
    help = \
        'Turn on flask application debugging.'
)
