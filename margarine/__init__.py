# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import argparse

import margarine.blend
import margarine.tinge
import margarine.spread

def run():
    parser = argparse.ArgumentParser(description = 'Margarine Wrapper')

    choices = ( 'blend', 'tinge', 'spread' )
    parser.add_argument('applications',
        nargs = '*',
        default = choices,
        choices = choices,
        help = 'List of margarine daemons to run. Default: %(default)s',
        metavar = 'APP'
    )

    arguments = parser.parse_args()

    for application in arguments.applications:
        getattr(margarine, application).run()
