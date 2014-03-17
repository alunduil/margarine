# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import uuid

from margarine.parameters import PARAMETERS

PARAMETERS.add_parameter(
    group = 'security',
    options = [ '--opaque' ],
    default = uuid.uuid4().hex,
    help = \
        'Opaque token used in HTTP digest authentication.  This should be set' \
        'to the same string on all blend servers that can interchangeably ' \
        'respond to requests.  Default random UUID4.'
)
