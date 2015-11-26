import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://172.16.0.134:%s" % port)

socket.send("client message to server1")

while True:
    socket.send("Server message to client3",zmq.NOBLOCK)
    msg = socket.recv()
    print msg
    time.sleep(1)
