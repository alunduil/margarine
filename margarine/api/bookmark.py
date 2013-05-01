# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from margarine.api import information
from margarine.api.application import APPLICATION

@APPLICATION.route('/{i.API_VERSION}/bookmarks/'.format(i = information))
def create_article():
    pass

@APPLICATION.route('/{i.API_VERSION}/bookmarks/<uuid>'.format(i = information))
def show_bookmark(uuid):
    pass

@APPLICATION.route('/{i.API_VERSION}/bookmarks/<uuid>/<property>'.format(i = information))
def show_bookmark_property(uuid, property):
    pass

