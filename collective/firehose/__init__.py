import zmq
import time


zmq_context = zmq.Context()
zmq_pub = zmq_context.socket(zmq.PUB)
zmq_pub.bind("ipc:///tmp/collective.firehose.sock")


def handle_start(event):
    start = time.time()
    request = event.request
    zmq_pub.send('%s %s' % (request.base + request.PATH_INFO, '+'))
    print str((time.time() - start) * 1e3) + 'ms'


def handle_end(event):
    request = event.request
    zmq_pub.send('%s %s' % (request.base + request.PATH_INFO, '-'))
