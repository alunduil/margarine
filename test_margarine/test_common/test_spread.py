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

UNMOCKED = {
    'datetime.datetime': datetime.datetime,
    'datetime.datetime.now': datetime.datetime.now,
    'datetime.datetime.utcnow': datetime.datetime.utcnow,
}


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

        self.mocked_datetime.side_effect = lambda *args, **kwargs: UNMOCKED['datetime.datetime'](*args, **kwargs)
        self.mocked_datetime.now.side_effect = lambda *args, **kwargs: UNMOCKED['datetime.datetime.now'](*args, **kwargs)
        self.mocked_datetime.utcnow.side_effect = lambda *args, **kwargs: UNMOCKED['datetime.datetime.utcnow'](*args, **kwargs)

        logger.info('STOPPING: mock datetime')

        return True

    mocks.add('tornado')

    def mock_tornado(self):
        logger.info('STARTING: mock tornado')

        if 'tornado' in self.mocks_mask:
            logger.info('STOPPING: mock tornado—MASKED')

            return False

        _ = mock.patch(self.real_module + '.tornado.httpclient.HTTPClient')

        self.addCleanup(_.stop)

        mocked_httpclient_constructer = _.start()

        self.mocked_httpclient = mock.MagicMock()
        mocked_httpclient_constructer.return_value = self.mocked_httpclient

        self.mocked_response = mock.MagicMock()
        self.mocked_httpclient.fetch.return_value = self.mocked_response

        logger.info('STOPPING: mock tornado')

        return True
