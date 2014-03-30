# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import logging
import mock
import re
import unittest

from test_margarine.test_fixtures.test_articles import ARTICLES

logger = logging.getLogger(__name__)


class BaseMargarineTest(unittest.TestCase):
    mocks_mask = set()
    mocks = set()

    def setUp(self):
        super(BaseMargarineTest, self).setUp()

        self.articles = copy.deepcopy(ARTICLES)

        for article in self.articles['all']:
            article['original_html'] = open(article['original_html'], 'r')

    @property
    def real_module(self):
        return re.sub(r'\.[^.]+', '', self.__module__.replace('test_', ''), 1)

    mocks.add('datastores')

    def mock_datastores(self):
        logger.info('STARTING: mock datastores')

        if 'datastores' in self.mocks_mask:
            logger.info('STOPPING: mock datastores—MASKED')

            return False

        logger.debug('self.real_module: %s', self.real_module)

        logger.debug('get_collection: %s', self.real_module + '.datastores.get_collection')
        _ = mock.patch(self.real_module + '.datastores.get_collection')

        self.addCleanup(_.stop)

        self.mocked_get_collection = _.start()

        self.mocked_collection = mock.MagicMock()
        self.mocked_get_collection.return_value = self.mocked_collection

        logger.debug('get_gridfs: %s', self.real_module + '.datastores.get_gridfs')
        _ = mock.patch(self.real_module + '.datastores.get_gridfs')

        self.addCleanup(_.stop)

        self.mocked_get_gridfs = _.start()

        self.mocked_gridfs = mock.MagicMock()
        self.mocked_get_gridfs.return_value = self.mocked_gridfs

        logger.info('STOPPING: mock datastores')

        return True

    mocks.add('queues')

    def mock_queues(self):
        logger.info('STARTING: mock queues')

        if 'queues' in self.mocks_mask:
            logger.info('STOPPING: mock queues—MASKED')

            return False

        logger.debug('producers: %s', self.real_module + '.kombu.pools.producers')
        _ = mock.patch(self.real_module + '.kombu.pools.producers')

        self.addCleanup(_.stop)

        self.mocked_producers = _.start()

        _1 = mock.MagicMock()
        self.mocked_producers.__getitem__.return_value = _1

        _2 = mock.MagicMock()
        _1.acquire.return_value = _2

        self.mocked_producer = mock.MagicMock()
        _2.__enter__.return_value = self.mocked_producer

        logger.info('STOPPING: mock queues')

        return True
