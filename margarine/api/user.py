# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from margarine.api import APPLICATION
from margarine.api import information

@APPLICATION.route('/{i.API_VERSION}/users/'.format(i = information))
def create_user():
    pass

@APPLICATION.route('/{i.API_VERSION}/users/<username>'.format(i = information))
def show_user(username):
    pass

@APPLICATION.route('{i.API_VERSION}/users/<username>/token'.format(i = information))
def show_user_login_token(username):
    pass

@APPLICATION.route('{i.API_VERSION}/users/<username>/<property>'.format(i = information))
def show_user_property(username, property):
    pass

