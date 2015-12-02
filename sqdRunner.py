
import sqdHelper as sqdH
from zmq_test.msgServer import msgServer
from zmq_test.msgClient import msgClient
import logging
import threading


# start cluster/leader
# add worker
# add client

logger = logging.getLogger("RunnerLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/Users/ajeetjha/zi/sqd/logs/runner.log")
handler.setFormatter(formatter)
logger.addHandler(handler)


class sqdRunner:

    def __init__(self):
        #initialize process ID to stop while they are running
        self.obj = dict()
        #self.processes = dict()

        self.obj["leader"] = None
        self.obj["worker"] = None
        self.obj["client"] = None
        self.obj["msgServer"] = None

        self.job_functions = {
            "leader": {
                "start": self.startLeaderRunner,
                "stop" : self.stopLeaderRunner

            },
            "worker": {
                "start": self.startWorkerRunner,
                "stop" : self.stopWorkerRunner

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

        # Simultaneously we Leader to do addWorker, which starts a msgClient at the worker's end
        pass

    def startWorkerRunner(self):
        pass

    def stopWorkerRunner(self):
        pass

    def stopWorker(self):
        pass

    def restartWorker(self):
        pass

    def doJob(self, msgD):
        logger.info("Doing job for: " + str(msgD))
        if msgD["op"] == "mode":
            print str(self.job_functions[msgD["args"][0]][msgD["args"][1]])
            self.job_functions[msgD["args"][0]][msgD["args"][1]]()

        if msgD["op"] == "leader":
            print str( self.obj["leader"].job_functions [msgD["args"][0]] [msgD["args"][1]] )
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
                #del msgObj.inbox[msgId]
                msgObj.inbox.pop(msgId,0)

                # [TODO] is any inbox message had time more than threshold, it must be removed.
        pass

    def reader(self):
        t = threading.Thread(target=self.cliMsgReader)
        t.daemon = True
        t.start()

    def startMsgServer(self, ip, port=None):
        self.obj["msgServer"] = msgServer(ip,port)

