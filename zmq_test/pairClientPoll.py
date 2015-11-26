import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://172.16.0.134:%s" % port)

#print "Sending 0..."
#socket.send("client message to server0")

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
poller.register(socket, zmq.POLLOUT)


while True:
    socks = dict(poller.poll())

    print"Printing poll result..."
    for obj in socks:
        print obj

    if socket in socks and socks[socket] == zmq.POLLIN:
        msg = socket.recv()
        print msg

    if socket in socks and socks[socket] == zmq.POLLOUT:
        print "Sending 1..."
        socket.send("client message to server1")



    time.sleep(1)