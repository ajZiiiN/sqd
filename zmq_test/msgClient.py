import zmq
import random
import sys
import time
import threading


class msgClient:
    def __init__(self):

        self.port = "5556"
        self.threads = []

        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.socket.connect("tcp://172.16.0.134:%s" % self.port)


    def recieve(self):

        while True:
            try:
                msg = self.socket.recv(zmq.NOBLOCK)
                print "Got: " + msg
            except zmq.ZMQError as e:
                print e
                print "Din recieve, Recovering...."
                time.sleep(5)
            except:
                print "[ERROR:recieve ] Something went Wrong.."
                return

    def send(self):

        while True:
            try:
                msgS = raw_input("MSG to send: ")
                self.socket.send(msgS, zmq.NOBLOCK)
            except zmq.ZMQError as e:
                print e
                print "Could not send, Recovering...."
                time.sleep(3)
            except:
                print "[ERROR:recieve ] Something went wrong.."
                return


    def run(self):

        self.socket.send("Heartbeat")
        t1 = threading.Thread(target=self.send)
        t1.start()
        self.threads.append(t1)

        t2 = threading.Thread(target=self.recieve)
        t2.start()
        self.threads.append(t2)

        for t in self.threads:
            t.join()