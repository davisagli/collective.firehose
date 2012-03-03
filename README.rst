collective.firehose
===================

The ZODB is great at storing document-oriented data. But it's pretty bad
at heavy-write scenarios, such as counting hits to create a list of most
popular pages.

``collective.firehose`` makes this sort of accounting possible by using
`0mq`_ to relay request start and end events to a separate process which
records hits in `redis`_.

(0mq is a brokerless message queue, which keeps needed infrastructure
to a minimum. Redis is a data structure server which is great at storing
the kind of data we need for this use case. Both are fast and this
architecture keeps overhead on the Zope instance tiny.)

.. _`0mq`: http://www.zeromq.org/
.. _`redis`: http://redis.io/

Installation
------------

You need libzmq and redis, with a running redis server.

E.g., pre-installation on OS X using homebrew::

  $ brew install redis zmq
  $ redis-server /usr/local/etc/redis.conf

In the buildout for your Plone site, you need to add collective.firehose
to your instance eggs::

  [instance]
  eggs = collective.firehose

And you also need to install the script which will relay request info to
redis::

  [buildout]
  parts += firehose

  [firehose]
  recipe = zc.recipe.egg
  eggs = collective.firehose

After running buildout, you should have a bin/firehose-record script. Run
this.

Finally, fire up your instance and go to http://localhost:8080/firehose-stats
You should see the stats update every 5 seconds as you navigate around the
site in another window.

If you are collecting stats from multiple Zope instances, you can make it
easier to identify which instance is serving a particular request by giving
each instance a unique identifier. Add to your buildout::

  [instance]
  zope-conf-additional =
    <product-config firehose>
        instance_id my-instance-id
    </product-config>

Retrieving statistics
---------------------

Stats can be retrieved using the redis client library. For example, here's
how the included stats view gets the top 10 most popular URLs for the
current hour::

  import redis
  import time

  # Get redis connection
  r = redis.StrictRedis(host='localhost', port=6379, db=0)

  # Calculate redis key for current hour
  timeslot = time.time() // 3600

  # Get the first 10 members of the "tophits" sorted set for the current hour.
  # ``tophits`` will be a list of (url, hit_count) tuples.
  tophits = r.zrevrange('tophits.%s' % timeslot, 0, 10, withscores=True)

Firehose stores in the following keys in redis:

  ``serving``
    A set of the URLs currently being served by Zope backends.

  ``tophits.[hour]``
    A sorted set of URLs accessed in the specified hour, scored by # of hits.
    The hour is given as the current Unix timestamp // 3600.

  ``elapsed.[hour]``
    A sorted set of URLs accessed in the specified hour, scored by the length
    of the slowest request for that URL.

Summarizing stats by periods of time larger than an hour should be possible
by periodically merging the hourly buckets. This is left as an exercise for the
pull-requester. ;-)
