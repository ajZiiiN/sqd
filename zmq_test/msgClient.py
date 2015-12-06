import zmq
import random
import sys
import time
import threading
import utils as u
from multiprocessing import Process
import logging


logger = u.getLogger("ClientLog", "/Users/ajeetjha/zi/sqd/logs/msgClient.log")

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
        self.keepRunning = True

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.connect("tcp://%s:%s" % (self.ip, self.port))


    def recieve(self):

        while self.keepRunning:
            try:
                logger.info("From Client (%s) Recieve..." %(self.ip,))
                #print "From Client Recieve.."

                msg = self.socket.recv(zmq.NOBLOCK)
                if msg != "Heartbeat":
                    id, msgDict = u.resolveMsg(msg)
                    logger.info("Id: " + str(id) + "  msgD: " + str(msgDict))
                    self.inbox[id] = msgDict

                #print "Client-Got: " + msg
                logger.info("Client-Got: " + msg)
            except zmq.ZMQError as e:
                logger.info(e)
                logger.info("Din recieve, Recovering....")
                time.sleep(2)
            except:
                logger.info(sys.exc_info()[0])
                logger.info("[Client-ERROR:recieve ] Something went Wrong..")
                return

    def send(self, msg=None):

        try:

            if msg == None:
                msgS = "MSG to send: "
            else:
                msgS = msg
            print "Client: sending..." ,msgS
            self.socket.send(msgS, zmq.NOBLOCK)

        except zmq.ZMQError as e:
            print e
            print "Could not send, Recovering...."
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

        t2 = threading.Thread(target=self.recieve)
        t2.daemon = True
        t2.start()
        self.threads.append(t2)


    def stop(self):
        self.keepRunning = False
        self.socket.close()
        self.context.term()
