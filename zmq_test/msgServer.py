import zmq
import random
import sys
import time
import thread
import threading
from multiprocessing import Process
import logging
import utils as u


logger = u.getLogger("ServerLog", "/Users/ajeetjha/zi/sqd/logs/msgServer.log")

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
        self.keepRunning = True

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)

        self.socket.bind("tcp://%s:%s" % (self.ip, self.port))



    def recieve(self):

        while self.keepRunning:
            try:
                logger.info("From Server (%s) Recieve.." % (self.ip,))
                #print "From Server Recieve.."

                msg = self.socket.recv(zmq.NOBLOCK)
                logger.info("Server-Got: " + msg)
                logger.info("Processing...")

                if msg != "Heartbeat":
                    id, msgDict = u.resolveMsg(msg)
                    logger.info("Id: " + str(id) + "  msgD: " + str(msgDict))
                    self.inbox[id] = msgDict
                logger.info("Processed...")


            except zmq.ZMQError as e:
                logger.info(e)
                logger.info("Server-Recieve: Din recieve, Recovering....")
                time.sleep(5)
                continue
            except:
                logger.info(sys.exc_info()[0])
                logger.info("Server-Recieve: Something went Wrong..")
                return


    def send(self, msg=None):

        try:
            if msg == None:
                msgS = "MSG to send: "
            else:
                msgS = msg

            print "Server: sending...", msgS
            self.socket.send(msgS, zmq.NOBLOCK)


        except zmq.ZMQError as e:
            print e
            print "Server-Send: Could not send, Recovering...."

        except:
            print "Server-Send: Something went wrong.."
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
        time.sleep(5)
        self.socket.close()
        self.context.term()

