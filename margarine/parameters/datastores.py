# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# margarine is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from margarine import information
from margarine.parameters import PARAMETERS

PARAMETERS.add_parameter(
    group = 'datastore',
    options = [ '--url' ],
    default = 'mongodb://localhost/test',
    help = 'URL of the datastore.  Default %(default)s.'
)

# =========================================================================== #
# See Also:                                                                   #
#   https://github.com/rackspace/pyrax/blob/master/docs/getting_started.md    #
# =========================================================================== #

PARAMETERS.add_parameter(
    group = 'pyrax',
    options = [ '--identity-type' ],
    default = 'rackspace',
    choices = [ 'rackspace', 'keystone' ],
    help = 'Identity type for pyrax.  Default %(default)s'
)

PARAMETERS.add_parameter(
    group = 'pyrax',
    options = [ '--auth-endpoint' ],
    help = 'Authentication endpoint for pyrax.  Default %(default)s'
)

PARAMETERS.add_parameter(
    group = 'pyrax',
    options = [ '--region' ],
    default = 'ORD',
    help = 'Region for pyrax (i.e. `dfw`, `ord`, `lon`, &c).  Default '
           '%(default)s'
)

PARAMETERS.add_parameter(
    group = 'pyrax',
    options = [ '--tenant-id' ],
    help = 'Tenant ID for pyrax authentication.  Used for `keystone` '
           'authentication.  Default %(default)s'
)

PARAMETERS.add_parameter(
    group = 'pyrax',
    options = [ '--tenant-name' ],
    help = 'Tenant name for pyrax authentication.  Used for `keystone` '
           'authentication.  Default %(default)s'
)

PARAMETERS.add_parameter(
    group = 'pyrax',
    options = [ '--custom-user-agent' ],
    default = 'Margarine-{i.VERSION}'.format(i = information),
    help = 'Custom User-Agent string for pyrax to use.  Default %(default)s'
)

PARAMETERS.add_parameter(
    group = 'pyrax',
    options = [ '--username' ],
    help = 'Username for pyrax authentication.'
)

PARAMETERS.add_parameter(
    group = 'pyrax',
    options = [ '--password' ],
    help = 'Password for pyrax authentication.  Used for `keystone` '
           'authentication.  Default %(default)s'
)

PARAMETERS.add_parameter(
    group = 'pyrax',
    options = [ '--api-key' ],
    help = 'API key for pyrax authentication.  Used for `rackspace` '
           'authentication.  Default %(default)s'
)
