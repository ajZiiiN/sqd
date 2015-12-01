import zmq
import random
import sys
import time
import threading
import utils
from multiprocessing import Process


class msgClient:
    def __init__(self, ip, port=None):

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
        self.socket.connect("tcp://%s:%s" % (self.ip, self.port))


    def recieve(self):

        while True:
            try:
                print "From Client Recieve.."

                poller = zmq.Poller()
                poller.register(self.socket, zmq.POLLIN)

                socks = dict(poller.poll())

                if self.socket in socks and socks[self.socket] == zmq.POLLIN:
                    msg = self.socket.recv(zmq.NOBLOCK)

                #id, msgDict = utils.resolveMsg(msg)
                #self.inbox[id] = msgDict

                print "Client-Got: " + msg
            except zmq.ZMQError as e:
                print e
                print "Din recieve, Recovering...."
                time.sleep(1)
                continue
            except:
                print "[Client-ERROR:recieve ] Something went Wrong.."
                return

    def send(self, msg=None):

        try:

            if msg == None:
                msgS = "MSG to send: "
            else:
                msgS = msg
            print "Client: sending..."
            self.socket.send(msgS, zmq.NOBLOCK)
            time.sleep(3)

        except zmq.ZMQError as e:
            print e
            print "Could not send, Recovering...."
            time.sleep(3)
        except:
            print "[Client-ERROR:recieve] Something went wrong.."
            return


    def run(self):

        self.socket.send("Heartbeat")
        '''
        t1 = Process(target=self.send)
        t1.start()
        self.threads.append(t1)
        '''

        t2 = Process(target=self.recieve)
        t2.start()
        self.threads.append(t2)


    def stop(self):
        for p in self.threads:
            p.terminate()

def getNewClient(ip, port=None):
    cli = msgClient(ip)

    cli.run()

    return cli



