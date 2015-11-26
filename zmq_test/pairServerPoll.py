import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://172.16.0.134:%s" % port)


poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
poller.register(socket, zmq.POLLOUT)

while True:

    socks = dict(poller.poll())

    print"Printing poll result..."
    for obj in socks:
        print obj

    if socket in socks and  socks[socket] == zmq.POLLOUT:
        print "Sending 3..."
        socket.send("Server message to client3")

    if socket in socks and socks[socket] == zmq.POLLIN:
        msg = socket.recv()
        print msg

    time.sleep(1)
