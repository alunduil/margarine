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
    * notations
    * text
    * parsed_at
    * votes
    * subscribers
    * original_etag

  * Notation

    * bookmark
    * location
    * note

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
  * Recent articles
  * Similar articles
  * Similar tags (fuzzy string match) [Not mappable and reducable]

Current Data Formats:

  * key/value
  * document
  * column family
  * graph
  * RDBMS

Column family is for massive tables (billions of rows and millions of columns).

Potential Data stores:

  * redis

    :cons: scalability, fault tolerance
    :pros: keys can be uuids and partitioning with replication

  * mongodb

    :cons: Objects as collections of documents (relations?)
    :pros: built-in map/reduce, auto-scaling (nearly)

    .. note::
        References are possible client-side:
        http://docs.mongodb.org/manual/reference/database-references/

  * hypergraphdb or neo4j

    :cons: only java implementations
    :pros: relationships are first-order items, graph theory!

  * postgresql

    :cons: difficult to scale (paritioning and slaves work though)
    :pros: ORM (SQLAlchemy)
  
"""

from flask import Flask

APPLICATION = Flask(__name__)

import errors
import user
import bookmark

