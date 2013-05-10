# -*- coding: UTF-8 -*-
#
# Copyright (C) 2013 by Alex Brandt <alex.brandt@rackspace.com>
#
# pycore is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

"""Main API application for Margarine.

Models:

  * User
  
    * uuid4
    * username
    * email
    * name
    * password → md5(username:realm:password)
    
  * Bookmark (never deleted) (just spider?)

    * uuid5(url)
    * url
    * text → sync to object store
    * tags
    * notations

      * location
      * note

    * votes
    * subscribers
     
      * uuid4
      * subscribed_at

    * created_at
    * original_etag
    * parsed_at

Simply normalize the above to get back to aggregate agnostic representations.

Data Requirements
-----------------

Reports:

  * Recommended articles (bookmarks) 

    Recommendations for new bookmarks use a neighbor function based on tags and
    subscribers.  A graph database would make this report ridiculously easy?

  * Recent articles (Ordering on bookmarks)
  * Similar articles [Not mappable and reducable?]
  * Similar tags (fuzzy string match) [Not mappable and reducable?]

Current Data Formats:

  * key/value
  * document
  * graph
  * column family (not appropriate due to the small column space)
  * RDBMS (doesn't lend to any parallel processing)

Parallelism in the larger reports would be nice but it's not obvious if this is
achievable or not.  More research into map/reduce algorithms is required to
determine if double loops lend themselves to this pattern.

Potential Data stores:

  * redis

    :cons: scalability, fault tolerance
    :pros: keys can be uuids and partitioning with replication

  * mongodb (likely candidate)

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

