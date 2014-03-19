# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from margarine.parameters import PARAMETERS

PARAMETERS.add_parameter(
    group = 'keystore',
    options = [ '--url' ],
    metavar = 'URL',
    default = 'redis://localhost',
    help = 'URL endpoint for the keystore where various tokens are kept.  '
           'Default %(default)s.'
)
