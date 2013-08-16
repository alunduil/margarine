# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

logger = logging.getLogger(__name__)

def power_of_units():
    '''Import unit tests and redfine to create base integration tests.

    An excellent start to an integration test suite is using the unit tests
    already defined.  Coupling this with a reduction in mocks following the
    powerset of all mocks used should generate a comprehensive integration
    suite as well as a basic functional suite (no mocks).  Using this idea this
    function imports all unit tests, the set of all mocks used, and generates
    the integration test suite.

    .. note::
        Integration tests can still be added by hand but probably should
        correlate to a unit test in all cases.

    '''

    pass
