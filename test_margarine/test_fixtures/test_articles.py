# -*- coding: UTF-8 -*-
#
# Copyright (C) 2014 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime

ARTICLES = {}

ARTICLES['correct'] = []

ARTICLES['correct'].append({
    'bson': {
        'cf_container_name': '0fb5c88e',
        'cf_object_name': '8753-5bc3-a251-4343b63682b0',
        'etag': '21696f99425b45b28ee9d2c308266beb',
        'original_url': 'http://developer.rackspace.com/blog/got-python-questions.html',
        'parsed_at': datetime.datetime(2014, 01, 26, 17, 35, 07, 217302),
        'updated_at': datetime.datetime(1994, 11, 15, 12, 45, 26, 000000),
    },
    'etag': '21696f99425b45b28ee9d2c308266beb',
    'json': {
        u'body': u'Mollit pork belly trust fund non. Occaecat hoodie jean shorts '
                 u'Neutra farm-to-table, actually whatever irure XOXO ea anim '
                 u'Truffaut chia. Cosby sweater nulla anim meh. Actually Vice '
                 u'cupidatat pour-over Odd Future, veniam nostrud distillery '
                 u'whatever aesthetic hella sunt church-key. Forage anim '
                 u'delectus iPhone seitan minim. Sartorial cardigan semiotics '
                 u'roof party proident VHS laboris, est shabby chic quis. Shabby '
                 u'chic keytar jean shorts hashtag sapiente, keffiyeh freegan '
                 u'bicycle rights Neutra labore cornhole actually beard enim.',
        u'etag': u'21696f99425b45b28ee9d2c308266beb',
        u'original_url': u'http://developer.rackspace.com/blog/got-python-questions.html',
        u'parsed_at': u'Sun, 26 Jan 2014 17:35:07.217302+0000',
        u'updated_at': u'Tue, 15 Nov 1994 12:45:26.000000+0000',
    },
    'updated_at': 'Tue, 15 Nov 1994 12:45:26 UTC',
    'url': 'http://developer.rackspace.com/blog/got-python-questions.html',
    'uuid': '0fb5c88e-8753-5bc3-a251-4343b63682b0',
})

ARTICLES['all'] = []

ARTICLES['all'].extend(ARTICLES['correct'])
