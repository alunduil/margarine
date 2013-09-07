# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from margarine.parameters import Parameters
from margarine.parameters.configuration import DIRECTORY as CONFIGURATION_DIRECTORY

Parameters('logging', parameters = [
    { # --logging-configuration=FILE; FILE ← CONFIGURATION_DIRECTORY/logging.ini
        'options': [ '--configuration' ],
        'default': os.path.join(CONFIGURATION_DIRECTORY, 'logging.ini'),
        'help': \
                'The configuration file containing the logging ' \
                'mechanism used by %(prog)s.  Default: %(default)s.',
        },
    ])

def configure_logging():
    '''Configure the system loggers using the Parameters' file provided.

    Uses Parameters[logging.configuration] to setup all logging mechanisms.

    '''

    logging_configuration_path = Parameters().parse(only_known = True)['logging.configuration']

    if os.access(logging_configuration_path, os.R_OK):
        logging.config.fileConfig(Parameters()['logging.configuration'])
