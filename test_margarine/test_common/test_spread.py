# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import logging
import mock

from test_margarine.test_common import BaseMargarineTest

logger = logging.getLogger(__name__)


class BaseSpreadTest(BaseMargarineTest):
    mocks_mask = set().union(BaseMargarineTest.mocks_mask)
    mocks = set().union(BaseMargarineTest.mocks)

    def setUp(self):
        super(BaseSpreadTest, self).setUp()

        self.mocked_message = mock.MagicMock()

    mocks.add('datetime')

    def mock_datetime(self):
        logger.info('STARTING: mock datetime')

        if 'datetime' in self.mocks_mask:
            logger.info('STOPPING: mock datetime—MASKED')

            return False

        logger.debug('datetime: %s', self.real_module + '.datetime.datetime')
        _ = mock.patch(self.real_module + '.datetime.datetime')

        self.addCleanup(_.stop)

        self.mocked_datetime = _.start()
        self.mocked_datetime.side_effect = lambda *args, **kwargs: datetime.datetime(*args, **kwargs)

        logger.info('STOPPING: mock datetime')

        return True
