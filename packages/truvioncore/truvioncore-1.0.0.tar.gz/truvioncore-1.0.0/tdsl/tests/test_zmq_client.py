
import zmq

if __name__ == '__main__':

	context = zmq.Context()

	#  Socket to talk to server
	print("Connecting to hello world server…")
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://localhost:5555")

	#  Do 10 requests, waiting each time for a response
	for request in range(10):
		print("Sending request %s …" % request)
		socket.send(b"Hello")

		#  Get the reply.
		message = socket.recv()
		print("Received reply %s [ %s ]" % (request, message))



	# txid = plpy.execute('SELECT txid_current() AS txid')[0]['txid']
	# payload = {
	#     'transaction': txid, 
	#     'event': TD['event'], 
	#     'table': TD['table_name'], 
	#     'old': TD['old'], 
	#     'new': TD['new']}
	# ctx = zmq.Context()
	# socket = ctx.socket(zmq.PUSH)
	# socket.connect("ipc:///tmp/zmq.sock")
	# socket.send(json.dumps(payload))
	# socket.close()
