# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from margarine.parameters import PARAMETERS

PARAMETERS.add_parameter(
    group = 'queue',
    options = [ '--url' ],
    default = 'amqp://guest:guest@localhost',
    help = 'The URL endpoint of the communication mechanism.  Default '
           '%(default)s'
)

PARAMETERS.add_parameter(
    group = 'queue',
    options = [ '--wait' ],
    default = 5,
    type = int,
    help = 'Number of seconds to wait between connection attempts to the '
           'communication mechanism.  Default %(default)s'
)
