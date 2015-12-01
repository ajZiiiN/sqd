import zmq
import random
import sys
import time
import thread
import threading
from multiprocessing import Process

class msgServer:

    def __init__(self, ip, port = None):
        if port == None:
            self.port = "5556"
        else:
            self.port = str(port)

        self.threads = []
        self.inbox = dict()
        self.outbox= dict()
        self.ip = ip

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)

        self.socket.bind("tcp://%s:%s" % (self.ip, self.port))



    def recieve(self):

        while True:
            try:
                print "From Server Recieve.."
                msg = self.socket.recv(zmq.NOBLOCK)

                #id, msgDict = utils.resolveMsg(msg)
                #self.inbox[id] = msgDict
                print "Server-Got: " + msg

            except zmq.ZMQError as e:
                print e
                print "Server-Recieve: Din recieve, Recovering...."
                time.sleep(1)
                continue
            except:
                print "Server-Recieve: Something went Wrong.."
                return

    def send(self, msg=None):
        while True:
            try:
                if msg == None:
                    msgS = "MSG to send: "
                else:
                    msgS = msg

                print "Server: sending..."
                self.socket.send(msgS, zmq.NOBLOCK)
                time.sleep(3)

            except zmq.ZMQError as e:
                print e
                print "Server-Send: Could not send, Recovering...."
                time.sleep(3)
            except:
                print "Server-Send: Something went wrong.."
                return


    def run(self):

        self.socket.send("Heartbeat")

        t1 = Process(target=self.send)
        t1.start()
        self.threads.append(t1)

        t2 = Process(target=self.recieve)
        t2.start()
        self.threads.append(t2)

        for t in self.threads:
            t.join()

    def stop(self):
        for p in self.threads:
            p.terminate()