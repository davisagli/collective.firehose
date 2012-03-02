import zmq
context = zmq.Context()
sub = context.socket(zmq.SUB)
sub.connect('ipc:///tmp/collective.firehose.sock')
sub.setsockopt(zmq.SUBSCRIBE, '')

while True:
    print sub.recv()
