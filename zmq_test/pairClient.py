import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://172.16.0.134:%s" % port)
socket.send("client message to server1")

while True:
    msg = socket.recv()
    print msg
    socket.send("client message to server1")
    socket.send("client message to server2")
    time.sleep(1)