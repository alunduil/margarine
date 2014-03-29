# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import tornado.testing

from test_margarine.test_common import BaseMargarineTest

from margarine.blend import BLEND_APPLICATION
from margarine.blend import information


class BaseBlendTest(BaseMargarineTest, tornado.testing.AsyncHTTPTestCase):
    mocks_mask = set().union(BaseMargarineTest.mocks_mask)
    mocks = set().union(BaseMargarineTest.mocks)

    def get_app(self):
        return BLEND_APPLICATION

    def setUp(self):
        super(BaseBlendTest, self).setUp()

        self.base_url = '/{i.API_VERSION}/articles/'.format(i = information)
