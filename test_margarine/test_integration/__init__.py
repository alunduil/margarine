# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import itertools

from test_margarine.test_unit import MARGARINE_MOCKS

logger = logging.getLogger(__name__)

def power_set(iterable):
    '''Generate the power set of the items contained in the iterable.

    Parameters
    ----------

    :``iterable``: the items to create the power set of

    Returns
    -------

    A generator that produces the elements of the power set of the passed
    iterable.

    '''

    logger.info('Generating Powerset')
    logger.debug('iterable: %s', iterable)

    for _ in xrange(len(iterable)):
        for combination in itertools.combinations(iterable, _):
            logger.debug('combination: %s', combination)

            yield combination

def power_of_units(units = ()):
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

    Parameters
    ----------

    :``units``: unit test classes to modify

    .. note::
        This method is specific to margarine's testing needs but could be
        generalized if the need arose.

    Returns
    -------

    A generator that produces tuples whose items are the derived class name and
    the class definition.

    '''

    for unit in units:
        logger.debug('unit: %s', unit)

        for mocks in power_set(MARGARINE_MOCKS):
            logger.debug('mocks: %s', mocks)
            logger.debug('unit.mock_mask: %s', unit.mock_mask)
            logger.debug('unit.__name__: %s', unit.__name__)

            if len(unit.mock_mask & mocks):
                name = unit.__name__.replace('Test', ''.join([ _.capitalize() for _ in mocks]) + 'Test')

                logger.debug('name: %s', name)

                def new_setUp(self):
                    '''Override setUp with skip dependant on running vagrant.

                    If a vagrant environment is not running or available.  We
                    should not run integration tests as dropping mocks will
                    only cause errors.

                    '''

                    super(self.__class__.__name__, self).setUp()

                    try:
                        output = subprocess.check_output([ 'vagrant', 'status' ])
                    except (subprocess.CalledProcessError,) as e:
                        logger.error('command failed: vagrant status')
                        logger.exception(e)

                    logger.debug('vagrant status: %s', output)

                    self.skipTest('Implement vagrant check')

                yield name, lambda: new.classobj(name, (unit,), {
                    'mocks': mocks,
                    'setUp': new_setUp,
                    })
