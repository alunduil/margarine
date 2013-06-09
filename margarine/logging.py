# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

from margarine.parameters import Parameters

Parameters("logging", parameters = [
    { # --logging-configuration=FILE; FILE ← CONFIGURATION_DIRECTORY/logging.conf
        "options": [ "--configuration" ],
        "default": os.path.join(CONFIGURATION_DIRECTORY, "logging.conf"),
        "help": \
                "The configuration file containing the logging " \
                "mechanism used by %(prog)s.  Default: %(default)s.",
        },
    ])

Parameters().parse(only_known = True)

logging.config.fileConfig(Parameters()["logging.configuration"])

