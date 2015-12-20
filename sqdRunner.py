
import sqdHelper as sqdH
from zmq_test.msgServer import msgServer
from zmq_test.msgClient import msgClient
import logging
import threading
import utils as u


# start cluster/leader
# add worker
# add client

logger = u.getLogger("RunnerLog", "/Users/ajeetjha/sandbox/sqd/logs/runner.log")


class sqdRunner:

    def __init__(self):
        #initialize process ID to stop while they are running
        self.obj = dict()
        #self.processes = dict()

        self.obj["leader"] = None
        self.obj["worker"] = None
        self.obj["client"] = None
        self.obj["msgServer"] = None # this is msgServer for CLI commands

        self.job_functions = {
            "leader": {
                "start": self.startLeaderRunner,
                "stop" : self.stopLeader

            },
            "worker": {
                "start": self.startWorkerRunner,
                "stop" : self.stopWorker

            },
            "client": {
                "start": self.startClientRunner,
                "stop" : self.stopClient

            }
        }


        pass



    def startLeader(self):

        logger.info("Starting Leader....")

        self.obj["leader"] = sqdH.sqdL()
        Leader = self.obj["leader"]

        # init cluster if new
        if Leader.leaderConfig["leader"]["new"] == True :
            Leader.initCluster()

        host = Leader.leaderConfig["leader"]["host"]

        for worker in Leader.leaderConfig["leader"]["workers"]:
            Leader.workers[worker] = msgClient(worker)
            Leader.workers[worker].run()

        Leader.reader()


        # Start subprocess for msgHandler

        # start a subprocess to handleMessages, pass leaderObject in it

        # create msg client for each workers and send ack to each one of them
        # Create a message dictionary for response maintaining all messages currently being sent and waiting for ack
        # create a worker on own host

        pass

    def startLeaderRunner(self):
        logger.info("Leader Runner... ")
        # start a subprocess for startLeader
        t = threading.Thread(target=self.startLeader)
        t.daemon = True
        t.start()

        pass

    def stopLeader(self):
        print "Stopping msgClients for Client..."
        clients = self.obj["leader"]["clients"].keys()
        for cl in clients:
            cl.stop()

        print "Stopping msgClients for Client..."

        workers = self.obj["leader"]["clients"].keys()
        for wo in workers:
            wo.stop()

        self.obj["leader"] = None
        pass

    def stopLeaderRunner(self):
        pass

    def restartLeader(self):
        pass

    def startWorker(self):
        # get a new sqdW object
        self.obj["worker"] = sqdH.sqdW()
        worker = self.obj["worker"]

        # if the worker is new worker
        if worker.workerConfig["worker"]["new"] == True:
            worker.initWorker()


        # start the msgServer
        host = worker.workerConfig["worker"]["host"]
        worker.msgObj = msgServer(host)

        print "Running worker msgServer..."
        worker.msgObj.run()

        print "Starting Readers..."
        worker.reader()

        # Simultaneously we Leader to do addWorker, which starts a msgClient at the worker's end
        pass

    def startWorkerRunner(self):

        logger.info("Worker Runner... ")
        # start a subprocess for startLeader
        t = threading.Thread(target=self.startWorker)
        t.daemon = True
        t.start()
        pass

    def stopWorker(self):
        print "Stopping worker msgServer..."
        self.obj["worker"].msgObj.stop()
        self.obj["worker"].stopCopy()
        self.obj["worker"] = None
        pass


    def restartWorker(self):
        pass

    def startClient(self):
        # get a new sqdW object
        self.obj["client"] = sqdH.sqdC()
        client = self.obj["client"]

        # if the worker is new worker
        if client.clientConfig["client"]["new"] == True:
            client.initClient()


        # start the msgServer
        host = client.clientConfig["client"]["host"]
        client.msgObj = msgServer(host)

        print "Running client msgServer..."
        client.msgObj.run()

        print "Starting Readers..."
        client.reader()

        # Simultaneously we Leader to do addClient, which starts a msgClient at the worker's end
        pass

    def startClientRunner(self):

        logger.info("Client Runner... ")
        # start a subprocess for startLeader
        t = threading.Thread(target=self.startClient)
        t.daemon = True
        t.start()
        pass

    def stopClient(self):
        print "Stopping client msgServer..."
        self.obj["client"].msgObj.stop()
        self.obj["client"] = None
        pass

    def doJob(self, msgD):
        logger.info("Doing job for: " + str(msgD))
        if msgD["op"] == "mode":
            print str(self.job_functions[msgD["args"][0]][msgD["args"][1]])
            self.job_functions[msgD["args"][0]][msgD["args"][1]]()

        if msgD["op"] == "leader":
            print str( self.obj["leader"].job_functions [msgD["args"][0]] [msgD["args"][2]] )
            self.obj["leader"].job_functions [msgD["args"][0]] [msgD["args"][2]](msgD["args"][1])
            # calling function with ip as argument

        if msgD["op"] == "status":
            pass
        pass


    def cliMsgReader(self):

        logger.info("Reading CLI messages....")
        while True:
            msgObj = self.obj["msgServer"]

            keys = msgObj.inbox.keys()
            for msgId in keys:
                logger.info("Reading CLI inbox....")
                M = msgObj.inbox
                self.doJob(msgObj.inbox[msgId])
                msgObj.inbox.pop(msgId,0)

                # [TODO] is any inbox message had time more than threshold, it must be removed.
        pass

    def reader(self):
        t = threading.Thread(target=self.cliMsgReader)
        t.daemon = True
        t.start()

    def startMsgServer(self, ip, port=None):
        self.obj["msgServer"] = msgServer(ip,port)

