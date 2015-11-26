import zmq
import random
import sys
import time
import threading

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://172.16.0.134:%s" % port)
socket.send("Heartbeat")

def recieve():

    while True:
        try:
            msg = socket.recv(zmq.NOBLOCK)
            print "Got: " + msg
        except zmq.ZMQError as e:
            print e
            print "Din recieve, Recovering...."
            time.sleep(5)
        except:
            print "[ERROR:recieve ] Something went Wrong.."
            return

def send():

    while True:
        try:
            msgS = raw_input("MSG to send: ")
            socket.send(msgS, zmq.NOBLOCK)
        except zmq.ZMQError as e:
            print e
            print "Could not send, Recovering...."
            time.sleep(3)
        except:
            print "[ERROR:recieve ] Something went wrong.."
            return


threads = []

t1 = threading.Thread(target=send)
t1.start()
threads.append(t1)

t2 = threading.Thread(target=recieve)
t2.start()
threads.append(t2)

for t in threads:
    t.join()