# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import os
import sys

from crumbs import Parameters

logger = logging.getLogger(__name__)

CONFIGURATION_DIRECTORY = os.path.join(os.path.sep, 'etc', 'margarine')

PARAMETERS = Parameters(conflict_handler = 'resolve') # TODO , inotify = True)

PARAMETERS.add_parameter(
    group = 'margarine',
    options = [ '--configuration-file-path', '-c' ],
    metavar = 'FILE',
    default = os.path.join(CONFIGURATION_DIRECTORY, 'margarine.ini'),
    help = \
        'Location of the configuration file containing margarine parameters.' \
        '  Default %(default)s'
)

PARAMETERS.add_parameter(
    group = 'logging',
    options = [ '--configuration-file-path' ],
    metavar = 'FILE',
    default = os.path.join(CONFIGURATION_DIRECTORY, 'logging.ini'),
    help = \
        'Location of the configuration file containing logging parameters.  ' \
        'Default %(default)s'
)

PARAMETERS.parse(only_known = True)

PARAMETERS.add_configuration_file(PARAMETERS['margarine.configuration_file_path'])

if os.access(PARAMETERS['logging.configuration_file_path'], os.R_OK):
    logging.config.fileConfig(PARAMETERS['logging.configuration_file_path'])
