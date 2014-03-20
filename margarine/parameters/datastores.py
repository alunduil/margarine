# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from margarine.parameters import PARAMETERS

PARAMETERS.add_parameter(
    group = 'datastore',
    options = [ '--url' ],
    default = 'mongodb://localhost/test',
    help = 'URL of the datastore.  Default %(default)s.'
)
