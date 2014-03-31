# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import logging
import mock
import unittest

from margarine import datastores

logger = logging.getLogger(__name__)


class BaseMargarineIntegrationTest(unittest.TestCase):
    mocks_mask = set()

    mocks_mask = mocks_mask.union('datastores')

    mocks = set()

    def setUp(self):
        super(BaseMargarineIntegrationTest, self).setUp()

        self.datastore_url = 'mongodb://192.0.2.7/test'

        if self.mock_parameters():
            parameters = {
                'datastore.url': self.datastore_url,
            }

            self.mocked_PARAMETERS.__getitem__.side_effect = lambda _: parameters[_]

        logger.info('cleaning datastores')
        datastores.get_collection('articles').remove()
        datastores.get_collection('fs').remove()

    mocks.add('parameters.PARAMETERS')

    def mock_parameters(self):
        if 'parameters.PARAMETERS' in self.mocks_mask:
            return False

        _ = mock.patch('margarine.datastores.PARAMETERS')

        self.addCleanup(_.stop)

        self.mocked_PARAMETERS = _.start()

        return True

    def add_fixture_to_datastore(self, fixture):
        grid = datastores.get_gridfs()
        fixture['bson']['body'] = grid.put(fixture['json']['body'], _id = fixture['bson']['body'], encoding = 'utf-8')
        self.addCleanup(functools.partial(grid.delete, fixture['bson']['body']))

        collection = datastores.get_collection('articles')
        collection.insert(fixture['bson'])
        self.addCleanup(functools.partial(collection.remove, fixture['bson']['_id']))
