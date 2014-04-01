# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import bson.objectid
import datetime
import os
import uuid

from test_margarine.test_fixtures import FIXTURE_DIRECTORY

ARTICLES = {}

ARTICLES['correct'] = []

ARTICLES['correct'].append({
    u'uuid': u'0fb5c88e-8753-5bc3-a251-4343b63682b0',
    u'url': u'http://developer.rackspace.com/blog/got-python-questions.html',

    u'response': {
        u'etag': u'cee086c837e3a8f3496addee84a2e136',
        u'html': unicode(open(os.path.join(FIXTURE_DIRECTORY, u'got-python-questions.html'), 'r').read(), 'utf-8'),
    },

    u'message_body': {
        u'pre_create': {
            u'url': u'http://developer.rackspace.com/blog/got-python-questions.html',
            u'uuid': uuid.UUID('0fb5c88e-8753-5bc3-a251-4343b63682b0'),
        },
        u'post_create': {
            u'uuid': uuid.UUID('0fb5c88e-8753-5bc3-a251-4343b63682b0'),
        },
    },

    u'bson': {
        u'post_create': {
            u'_id': u'0fb5c88e87535bc3a2514343b63682b0',
            u'created_at': datetime.datetime(1994, 11, 15, 12, 45, 26, 000000),
            u'original_url': u'http://developer.rackspace.com/blog/got-python-questions.html',
            u'updated_at': datetime.datetime(2014, 1, 26, 17, 35, 7, 217000),
        },
        u'post_sanitize': {
            u'body': bson.objectid.ObjectId('532f29a14ee7ca6d41afae50'),
            u'etag': u'd0dbbb6ba01a95c3bfeca3f46e3d15b03873fff4a4b780700c8bc23994329f0f',
            u'original_etag': u'cee086c837e3a8f3496addee84a2e136',
            u'parsed_at': datetime.datetime(2014, 1, 26, 17, 35, 7, 217000),
            u'updated_at': datetime.datetime(2014, 1, 26, 17, 35, 7, 217000),
        },
    },

    u'generated_headers': {
        u'etag': u'd0dbbb6ba01a95c3bfeca3f46e3d15b03873fff4a4b780700c8bc23994329f0f',
        u'last_modified': u'Sun, 26 Jan 2014 17:35:07 UTC',
    },
    u'json': {
        u'_id': u'0fb5c88e87535bc3a2514343b63682b0',
        u'body': unicode(open(os.path.join(FIXTURE_DIRECTORY, 'got-python-questions.html.sanitized'), 'r').read(), 'utf-8'),
        u'created_at': u'Tue, 15 Nov 1994 12:45:26.000000+0000',
        u'etag': u'd0dbbb6ba01a95c3bfeca3f46e3d15b03873fff4a4b780700c8bc23994329f0f',
        u'original_etag': u'cee086c837e3a8f3496addee84a2e136',
        u'original_url': u'http://developer.rackspace.com/blog/got-python-questions.html',
        u'parsed_at': u'Sun, 26 Jan 2014 17:35:07.217000+0000',
        u'updated_at': u'Sun, 26 Jan 2014 17:35:07.217000+0000',
    },
})

ARTICLES['all'] = []

ARTICLES['all'].extend(ARTICLES['correct'])
