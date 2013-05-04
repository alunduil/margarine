# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""Main API application for Margarine.

Models:

  * User
  
    * username
    * email
    * name
    * password → md5(username:realm:password)
    * bookmarks (ordered list of bookmark submissions)
    
  * Bookmark (never deleted) (just spider?)

    * url
    * tags
    * text
    * parsed_at
    * votes
    * subscribers
    * original_etag

  * Tag (need to be a separate collection?)
    
    * name
    * similar (fuzzy matching)
    * bundle (category?)

The data looks relational at first glance but that doesn't require a relational
system to maintain it.

Recommendations for new bookmarks use a neighbor function based on tag edges
and subscriber edges.  Graph database for this type of report.

Accessing the objects themselves…doesn't matter?

De-normalizing required to use a non-RDBMS?

Data Requirements
-----------------

Reports:

  * Recommended articles (bookmarks)

Current Data Formats:

  * key/value
  * document
  * column family
  * graph
  * RDBMS

Potential Data stores:

  * redis
  
"""

from flask import Flask

APPLICATION = Flask(__name__)

import errors
import user
import bookmark

