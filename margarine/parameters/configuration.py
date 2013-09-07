# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

from margarine.parameters import Parameters

logger = logging.getLogger(__name__)

DIRECTORY = os.path.join(os.path.sep, 'etc', 'margarine')
FILE = os.path.join(DIRECTORY, 'margarine.ini')

Parameters(parameters = [
    { # --configuration=FILE, -f=FILE; FILE ← FILE
        'options': [ '--configuration', '-f' ],
        'default': FILE,
        'help': \
                'Configuration file to use to configure %(prog)s as a whole.',
        },
    ])

Parameters(file_path = Parameters().parse(only_known = True)['configuration'])
