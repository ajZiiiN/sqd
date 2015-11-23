import zmq
import time

print zmq.pyzmq_version() 
context = zmq.Context()
print context