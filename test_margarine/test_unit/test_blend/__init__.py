# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest
import mock

import logging

from test_margarine.test_unit import BaseMargarineTest

from margarine.blend import information
from margarine.blend import BLEND

logger = logging.getLogger(__name__)

class BaseBlendTest(BaseMargarineTest):
    def setUp(self):
        super(BaseBlendTest, self).setUp()

        BLEND.config['TESTING'] = True
        self.application = BLEND.test_client()

