# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import json
import logging
import time
import tornado
import unittest
import urllib

from test_margarine import test_helpers
from test_margarine.test_common.test_blend import BaseBlendTest

logger = logging.getLogger(__name__)


@unittest.skipUnless(test_helpers.is_vagrant_up('datastore'), 'vagrant up datastore')
@unittest.skipUnless(test_helpers.is_vagrant_up('queue'), 'vagrant up queue')
@unittest.skipUnless(test_helpers.is_vagrant_up('spread'), 'vagrant up spread')
@unittest.skipUnless(test_helpers.is_vagrant_up('blend'), 'vagrant up blend')
class BlendArticleSystemTest(BaseBlendTest):
    mocks_mask = set().union(BaseBlendTest.mocks_mask)
    mocks = set().union(BaseBlendTest.mocks)

    def setUp(self):
        super(BlendArticleSystemTest, self).setUp()

        self.client = tornado.httpclient.HTTPClient()

        self.url = 'http://192.0.2.3:5000' + self.base_url

    def test_article_create_read(self):
        '''blend.articles—POST   /articles/?article_url=? → 202 and GET    /articles/? → 200'''

        for article in self.articles['all']:
            response = self.client.fetch(self.url, method = 'POST', body = urllib.urlencode({ 'article_url': article['url'] }))

            self.assertEqual(202, response.code)

            time.sleep(1)  # Pause for effect…

            response = self.client.fetch(self.url + article['uuid'], method = 'GET')

            self.assertEqual(200, response.code)

            body = json.loads(response.body)

            self.assertIn('body', body)
            self.assertNotEqual(0, len(body['body']))
