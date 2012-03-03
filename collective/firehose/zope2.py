import time
import threading
import redis
import zmq
from Products.Five import BrowserView

STATS = threading.local()

zmq_context = zmq.Context()
zmq_pub = zmq_context.socket(zmq.PUB)
zmq_pub.connect("ipc:///tmp/collective.firehose.sock")


def handle_start(event):
    request = event.request
    STATS.start = time.time()
    # XXX should include instance id
    zmq_pub.send('%s %s' % (request.base + request.PATH_INFO, 0))


def handle_end(event):
    request = event.request
    zmq_pub.send('%s %s' % (request.base + request.PATH_INFO, time.time() - STATS.start))


class StatsView(BrowserView):

	def update(self):
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		pipe = r.pipeline()

		timeslot = time.time() // 3600
		pipe.smembers('serving')
		pipe.zrevrange('tophits.%s' % timeslot, 0, 10, withscores=True, score_cast_func=int)
		pipe.zrevrange('elapsed.%s' % timeslot, 0, 10, withscores=True)

		self.serving, self.tophits, self.elapsed = pipe.execute()

	def __call__(self):
		self.update()
		return self.index()


# What data do I want to fetch?
# 1. What URL is each client serving right now -- set of client:URL
# 2. What are the most popular URLs? -- sorted set of URL scored by weight
# 3. What are the most popular URLs within the past hour? -- sorted set of URLs scored by weight for each hour + cron job that updates a union of the past N buckets
# 4. What are the slowest URLs? -- sorted set of URLs scored by request time
