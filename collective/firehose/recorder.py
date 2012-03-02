import time
import redis
import zmq


def record_stats():

	try:
		context = zmq.Context()
		sub = context.socket(zmq.SUB)
		sub.connect('ipc:///tmp/collective.firehose.sock')
		sub.setsockopt(zmq.SUBSCRIBE, '')

		r = redis.StrictRedis(host='localhost', port=6379, db=0)


		while True:
		    url, elapsed = sub.recv().rsplit(' ', 1)
		    pipe = r.pipeline()

		    # track current requests
		    if elapsed == '0':
		    	pipe.sadd('serving', url)
		    else:
		    	pipe.srem('serving', url)

			    # track top hits per hour
			    timeslot = time.time() // 3600
			    pipe.zincrby('tophits.%s' % timeslot, url, 1)

			    # track slowest hits per hour (in ms)
			    slowkey = 'elapsed.%s' % timeslot
			    old_elapsed = r.zscore(slowkey, url)
			    if old_elapsed is None or float(elapsed) > float(old_elapsed):
			    	pipe.zincrby(slowkey, url, elapsed)

		    pipe.execute()
	except (KeyboardInterrupt, SystemExit):
		pass
	except:
		raise
	finally:
		sub.close()

# What data do I want to fetch?
# 1. What URL is each client serving right now -- set of client:URL
# 2. What are the most popular URLs? -- sorted set of URL scored by weight
# 3. What are the most popular URLs within the past hour? -- sorted set of URLs scored by weight for each hour + cron job that updates a union of the past N buckets
# 4. What are the slowest URLs? -- sorted set of URLs scored by request time
