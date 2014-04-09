# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import bson
import functools
import kombu
import logging
import mock
import unittest

from test_margarine import test_helpers

from margarine import datastores
from margarine import queues

logger = logging.getLogger(__name__)


class BaseMargarineIntegrationTest(unittest.TestCase):
    mocks_mask = set()
    mocks = set()

    def setUp(self):
        super(BaseMargarineIntegrationTest, self).setUp()

        self.parameters = {}

    mocks.add('parameters.PARAMETERS')

    def mock_parameters(self):
        if 'parameters.PARAMETERS' in self.mocks_mask:
            return False

        _ = mock.patch('margarine.{0}s.PARAMETERS'.format(self.component))

        self.addCleanup(_.stop)

        self.mocked_PARAMETERS = _.start()

        return True


@unittest.skipUnless(test_helpers.Box('datastore').is_up, 'vagrant up datastore')
class BaseDatastoreIntegrationTest(BaseMargarineIntegrationTest):
    mocks_mask = set()
    mocks_mask = mocks_mask.union(BaseMargarineIntegrationTest.mocks_mask)
    mocks_mask = mocks_mask.union('datastores')

    mocks = set()
    mocks = mocks.union(BaseMargarineIntegrationTest.mocks)

    def setUp(self):
        super(BaseDatastoreIntegrationTest, self).setUp()

        self.component = 'datastore'

        self.datastore_url = 'mongodb://192.0.2.7/test'

        self.parameters['datastore.url'] = self.datastore_url

        if self.mock_parameters():
            self.mocked_PARAMETERS.__getitem__.side_effect = lambda _: self.parameters[_]

        logger.info('cleaning datastores')

        datastores.get_collection('articles').remove()
        datastores.get_collection('fs').remove()

    def add_fixture_to_datastore(self, fixture, body = None):
        logger.info('STARTING: add fixture %s', fixture['_id'])

        if body is not None:
            grid = datastores.get_gridfs()

            if isinstance(body, bson.objectid.ObjectId):
                logger.info('wrapping gridfs')

                _ = mock.patch(self.real_module + '.datastores.get_gridfs')

                self.addCleanup(_.stop)

                self.mocked_get_gridfs = _.start()
                self.mocked_get_gridfs.return_value = grid

                original_put = grid.put

                grid.put = lambda *args, **kwargs: original_put(_id = body, *args, **kwargs)
                self.addCleanup(functools.partial(grid.delete, body))
            else:
                logger.info('adding gridfs fixture')

                fixture['body'] = grid.put(body, _id = fixture['body'], encoding = 'utf-8')
                self.addCleanup(functools.partial(grid.delete, fixture['body']))

        collection = datastores.get_collection('articles')
        collection.insert(fixture)
        self.addCleanup(functools.partial(collection.remove, fixture['_id']))

        logger.info('STOPPING: add fixture %s', fixture['_id'])


@unittest.skipUnless(test_helpers.Box('queue').is_up, 'vagrant up queue')
class BaseQueueIntegrationTest(BaseMargarineIntegrationTest):
    mocks_mask = set()
    mocks_mask = mocks_mask.union(BaseMargarineIntegrationTest.mocks_mask)
    mocks_mask = mocks_mask.union('queues')

    mocks = set()
    mocks = mocks.union(BaseMargarineIntegrationTest.mocks)

    def setUp(self):
        super(BaseQueueIntegrationTest, self).setUp()

        self.component = 'queue'

        if test_helpers.Box('spread').is_up:
            test_helpers.Box('spread').destroy()
            self.addCleanup(test_helpers.Box('spread').up)

        self.queue_url = 'amqp://guest:guest@192.0.2.5'

        self.parameters['queue.url'] = self.queue_url

        if self.mock_parameters():
            self.mocked_PARAMETERS.__getitem__.side_effect = lambda _: self.parameters[_]

    def intercept_message(self, queue, timeout = 1):
        _ = queues.get_connection().SimpleQueue(queue, serializer = 'pickle')

        self.addCleanup(_.clear)

        _.consumer.accept = kombu.serialization.prepare_accept_content(['pickle'])
        return _.get(timeout = timeout).payload
