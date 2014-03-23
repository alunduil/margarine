# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import tornado.testing

from test_margarine.test_fixtures.test_articles import ARTICLES

from margarine.blend import BLEND_APPLICATION
from margarine.blend import information


class BaseBlendTest(tornado.testing.AsyncHTTPTestCase):
    mocks_mask = set()
    mocks = set()

    def get_app(self):
        return BLEND_APPLICATION

    def setUp(self):
        super(BaseBlendTest, self).setUp()

        self.articles = copy.deepcopy(ARTICLES)

        self.base_url = '/{i.API_VERSION}/articles/'.format(i = information)
