# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import itertools
import subprocess
import new
import os
import sys
import re
import importlib
import inspect

from test_margarine.test_unit import MARGARINE_MOCKS
from test_margarine.test_unit import BaseMargarineTest

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

def integrated_units(units = ()):
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

def find_units(unit_paths = ( os.path.join('..', 'test_unit'), )):
    '''Find all units in the specified directories.

    Find all of the unit tests defined in the passed list of directories.  The
    default search path is the peer directory of this one, test_unit.

    Parameters
    ----------

    :``unit_paths``: list of paths to search for unit tests

    Returns
    -------

    List of units that can be manipulated to create integration tests.

    '''

    units = []

    temporary_paths = []

    path = unit_paths

    for directory in path:
        logger.info('Searching %s for units…', directory)

        if not os.access(directory, os.R_OK):
            continue

        if directory not in sys.path:
            temporary_paths.append(directory)
            sys.path.insert(0, directory)

        walk = list(os.walk(directory))

        filenames = []
        filenames.extend(itertools.chain(*[ [ os.path.join(file_[0], name) for name in file_[1] ] for file_ in walk if len(file_[1])]))
        filenames.extend(itertools.chain(*[ [ os.path.join(file_[0], name) for name in file_[2] ] for file_ in walk if len(file_[2])]))
        filenames = list(set([ filename.replace(directory + '/', '') for filename in filenames if '/.' not in filename ]))

        module_names = list(set([ re.sub(r'\.py.?', '', filename).replace('/', '.') for filename in filenames if not re.search(r'(/|^)_', filename) ]))

        modules = []

        for module_name in module_names:
            try:
                modules.append(importlib.import_module(module_name))
                logger.info('Module, %s, imported', module_name)
            except (ImportError,) as e:
                logger.warning('Module, %s, not able to be imported', module_name)
                logger.exception(e)
                continue

        for module in modules:
            for class_ in inspect.getmembers(module, inspect.isclass):
                if issubclass(class_, BaseMargarineTest) and not class_.__name__.startswith('Base'):
                    logger.info('Recording unit, %s', class_.__name__)
                    units.append(class_)

    return units
