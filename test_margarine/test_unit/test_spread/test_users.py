# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import mock
import logging
import json
import pymongo
import datetime

from test_margarine.test_unit.test_spread import BaseSpreadTest

# TODO Remove pluralization of users
from margarine.spread.users import create_user_consumer
from margarine.spread.users import password_email_consumer
from margarine.spread.users import update_user_consumer

logger = logging.getLogger(__name__)

class BaseSpreadUserTest(BaseSpreadTest):
    # TODO A better way to write this?
    mock_mask = BaseSpreadTest.mock_mask | set([
        'channel',
        'container',
        ])

    def setUp(self):
        super(BaseSpreadUserTest, self).setUp()

        # TODO Merge with accounts from test_blend.test_user?
        self.accounts = {
                'alunduil': { 'email': 'alunduil@alunduil.com', },
                }

        self.method = mock.MagicMock()

        self.test_datetime = datetime.datetime(2013, 8, 7, 20, 25, 41, 596627)

class SpreadUserCreateTest(BaseSpreadUserTest):
    def setUp(self):
        super(SpreadUserCreateTest, self).setUp()

        self.method.delivery_tag.return_value = 'create'

    def test_user_create_unsubmitted(self):
        '''Spread::User Create—Unsubmitted

        .. note::
            Tests first submission of the user (nothing stored yet).

        '''

        for username, properties in self.accounts.iteritems():
            with mock.patch('.'.join([
                self.__module__.replace('test_', '').replace('unit.', ''),
                'password_email_consumer',
                ])) as mock_password_email_consumer:

                # TODO Add more tests for exceptions from mock_password_email_consumer
                # TODO Couple with upper layer by sharing message
                args = [
                        mock.MagicMock(),
                        self.method,
                        None,
                        json.dumps(properties),
                        ]

                create_user_consumer(*args)

                mock_password_email_consumer.assert_called_once_with(*args)

            self.mock_collection.insert.assert_called_once_with(properties)
            self.mock_collection.reset_mock()

    def test_user_create_submitted_complete(self):
        '''Spread::User Create—Submitted,Complete

        .. note::
            The user is being resubmitted after all components have run.

        If two or more requests occur simultaneously, the secondary and
        subsequent requests are silently ignored.  Simultaneous is defined as
        the time between the first request for a username being accepted and
        the first user information being written to the datastore.

        '''

        for username, properties in self.accounts.iteritems():
            self.mock_collection.insert.side_effect = pymongo.errors.DuplicateKeyError

            args = [
                    mock.MagicMock(),
                    self.method,
                    None,
                    json.dumps(properties),
                    ]

            create_user_consumer(*args)

            self.mock_collection.insert.assert_called_once_with(json.dumps(properties))
            self.mock_collection.reset_mock()

            # TODO Handle duplicate requests differently?

class SpreadUserUpdateTest(BaseSpreadUserTest):
    '''Spread::User Update

    .. note::
        This will never be invoked unless a delete finished before the update
        message is processed.

        This should be verified for correctness.

    '''

    def setUp(self):
        super(SpreadUserUpdateTest, self).setUp()

        self.method.delivery_tag.return_value = 'update'

    def test_user_update(self):
        '''Spread::User Update'''

        modifications = {
                'alunduil': { 'name': 'Alex Brandt', },
                }

        for username, properties in self.accounts.iteritems():
            update_user_consumer(mock.MagicMock(), self.method, None, json.dumps(modifications[username]))

            self.mock_collection.update.assert_called_once_with({ 'username': username }, { '$set': modifications[username] }, upsert = True)
            self.mock_collection.reset_mock()

class SpreadPasswordEmailTest(BaseSpreadUserTest):
    def setUp(self):
        super(SpreadPasswordEmailTest, self).setUp()

        self.method.delivery_tag.return_value = 'email.password'

    def test_user_password_email(self):
        '''Spread::User Password Email'''

        for username, properties in self.accounts:
            password_email_consumer(mock.MagicMock(), self.method, None, json.dumps(properties))

            self.fail('Complete Stub!')

class SpreadPasswordChangeTest(BaseSpreadUserTest):
    def setUp(self):
        super(SpreadPasswordChangeTest, self).setUp()

        self.method.delivery_tag.return_value = 'change.password'

    def test_user_password_change(self):
        '''Spread::User Password Change'''

        for username, properties in self.accounts:
            self.fail('Complete Stub!')
