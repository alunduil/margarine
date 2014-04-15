# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
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
    options = [ '--retries' ],
    default = 3,
    type = int,
    help = 'Number of times to automatically retry publishing messages.  '
           'Default %(default)s'
)
