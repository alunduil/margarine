# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import gridfs
import mock
import pymongo
import unittest


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

    mocks.add('parameters.PARAMETERS')

    def mock_parameters(self):
        if 'parameters.PARAMETERS' in self.mocks_mask:
            return False

        _ = mock.patch('margarine.datastores.PARAMETERS')

        self.addCleanup(_.stop)

        self.mocked_PARAMETERS = _.start()

        return True

    def add_fixture_to_datastore(self, fixture):
        database = pymongo.MongoClient(self.datastore_url)[self.datastore_url.rsplit('/', 1)[-1]]

        grid = gridfs.GridFS(database)

        fixture['bson']['body'] = grid.put(fixture['json']['body'], _id = fixture['bson']['body'], encoding = 'utf-8')

        self.addCleanup(functools.partial(grid.delete, fixture['bson']['body']))

        database['articles'].insert(fixture['bson'])

        self.addCleanup(functools.partial(database['articles'].remove, fixture['bson']['_id']))
