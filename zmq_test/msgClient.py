import zmq
import random
import sys
import time
import threading
import utils
from multiprocessing import Process
import logging

logger = logging.getLogger("ClientLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/Users/ajeetjha/zi/sqd/logs/msgClient.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

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
                logger.info("From Client Recieve..")
                #print "From Client Recieve.."

                msg = self.socket.recv(zmq.NOBLOCK)

                #id, msgDict = utils.resolveMsg(msg)
                #self.inbox[id] = msgDict

                #print "Client-Got: " + msg
                logger.info("Client-Got: " + msg)
                time.sleep(5)
            except zmq.ZMQError as e:
                logger.info(e)
                logger.info("Din recieve, Recovering....")
                time.sleep(5)
            except:
                logger.info("[Client-ERROR:recieve ] Something went Wrong..")
                return

    def send(self, msg=None):

        try:

            if msg == None:
                msgS = "MSG to send: "
            else:
                msgS = msg
            print "Client: sending..."
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
        for p in self.threads:
            p.terminate()

def getNewClient(ip, port=None):
    cli = msgClient(ip)

    #cli.run()

    return cli



