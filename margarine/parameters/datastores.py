# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

from margarine.parameters import Parameters
from margarine.paraemters.configuration import DIRECTORY as CONFIGURATION_DIRECTORY

Parameters('datastore', parameters = [
    { # --datastore-url=URL; URL ← mongodb://localhost/test
        'options': [ '--url' ],
        'default': 'mongodb://localhost/test',
        'help': \
                'The URL endpoint of the data store mechanism.  This ' \
                'defaults to a mongo instance running on the localhost but ' \
                'can also be another datastore such as: couchdb, neo4j, &c. ',
        }
    ])

# TODO Make this more consistent with the rest of the parameters.
Parameters('pyrax', parameters = [
    { # --pyrax-credentials-file=FILE; FILE ← CONFIGURATION_DIRECTORY/pyrax.ini
        'options': [ '--credentials-file' ],
        'default': os.path.join(CONFIGURATION_DIRECTORY, 'pyrax.ini'),
        'help': \
                'The configuration file containing the pyrax credentials ' \
                'used by %(prog)s.  Default: %(default)s.',
        },
    { # --pyrax-identity-type=TYPE; TYPE ← rackspace
        'options': [ '--identity-type' ],
        'default': 'rackspace',
        'help': \
                'The identity type for pyrax.  This needs to be set outside ' \
                'of the pyrax configuration due to the pyrax ' \
                'implementation.  This defaults to %(default)s but can be ' \
                'over-ridden if required.',
        },
    ])
