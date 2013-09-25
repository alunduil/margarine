# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

from test_margarine.test_unit.test_blend import BaseBlendTest

from margarine.blend import information

logger = logging.getLogger(__name__)

class BaseBlendTagTest(BaseBlendTest):
    def setUp(self):
        super(BaseBlendTagTest, self).setUp()

        self.tags = []

        self.base_url = '/{i.API_VERSION}/tags/'.format(i = information)
