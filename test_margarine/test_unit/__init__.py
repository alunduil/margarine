# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest
import mock

import logging

logger = logging.getLogger(__name__)

MARGARINE_MOCKS = set([
    'channel',
    'collection',
    'keyspace',
    'container',
    ])

class BaseMargarineTest(unittest.TestCase):
    mocks = MARGARINE_MOCKS
    mock_mask = set()

    def setUp(self):
        super(BaseMargarineTest, self).setUp()

        self._set_up_mocks(self.mock_mask)

    def _get_patch_mock(self, mock_function):
        '''Patch and return a mock for the specified function.

        Correlates to the currently running test to streamline patching local
        and mocking items.

        Arguments
        ---------

        :``mock_function``: The function name to mock in the local module scope

        '''

        patcher = mock.patch('.'.join([
            # TODO Also handle integration and functional suites.
            self.__module__.replace('test_', '').replace('unit.', ''),
            mock_function,
            ]))

        self.addCleanup(patcher.stop)

        return patcher.start()

    def _get_attached_mock(self, mock_function):
        '''Attach a mock to the return value of the mock_function.

        It's common (in this application anyway) to need to mock the return
        value of a function rather than just the function itself.  This
        function factors that idiom out into one location.

        Arguments
        ---------

        :``mock_function``: The mock that we are overriding the return value of

        '''

        _ = mock_function
        desired_mock = mock.MagicMock()
        _.return_value = desired_mock

        return desired_mock

    def _set_up_mocks(self, mock_mask = ()):
        '''Set up all mocks except those specified in the mock_mask.

        Sets up all mocks required by margarine except those mocks that are
        specified in the mock mask (read from self.mock_mask in setUp if
        present).

        Arguments
        ---------

        :``mock_mask``: The list of mocks to not setup.  Used for controlling
                        what portions are not mocked during integration and
                        functional testing.

        '''

        # TODO Reduce cyclomatic complexity here.

        logger.debug('mocks: %s', self.mocks)
        logger.debug('mock_mask: %s', self.mock_mask)
        logger.debug('to_mock: %s', self.mocks - self.mock_mask)

        to_mock = self.mocks - self.mock_mask

        if 'channel' in to_mock:
            self.mock_channel = self._get_attached_mock(self._get_patch_mock('get_channel'))

        # TODO Update to datastores
        if 'collection' in to_mock:
            self.mock_collection = self._get_attached_mock(self._get_patch_mock('get_collection'))

        # TODO Update to datastores
        if 'keyspace' in to_mock:
            self.mock_keyspace = self._get_attached_mock(self._get_patch_mock('get_keyspace'))

        # TODO Update to datastores
        if 'container' in to_mock:
            self.mock_container = self._get_attached_mock(self._get_patch_mock('get_container'))
