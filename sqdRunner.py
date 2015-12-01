
import sqdHelper as sqdH
from zmq_test.msgServer import msgServer
from zmq_test.msgClient import msgClient


# start cluster/leader
# add worker
# add client



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
        # get new sqdL object
        Leader = sqdH.sqdL()
        self.obj["leader"] = Leader

        # init cluster if new
        if Leader.leaderConfig["new"] == True :
            Leader.initCluster()



        # handle difference between new and and existing cluster
        # is config is new, initCluster
        host = Leader.leaderConfig["leader"]["host"]

        for worker in Leader.leaderConfig["leader"]["workers"]:
            Leader.workers[worker] = msgClient()
            Leader.workers[worker].run()

        # for each worker , add that worker
            # while adding, start a msgClient for that worker
            # store in leader.workers
            # run each msgClient

        # Start subprocess for msgHandler

        # start a subprocess to handleMessages, pass leaderObject in it

        # create msg client for each workers and send ack to each one of them
        # Create a message dictionary for response maintaining all messages currently being sent and waiting for ack
        # create a worker on own host

        pass

    def startLeaderRunner(self):

        # start a subprocess for startLeader
        pass

    def stopLeader(self):
        pass

    def stopLeaderRunner(self):
        pass

    def restartLeader(self):
        pass

    def startWorker(self):
        # get a new sqdW object
        worker = sqdH.sqdW()

        if worker.workerConfig["worker"]["new"] == True:
            worker.initWorker()

        # if the worker is new worker
        # init it

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

    def doJob(self, msg):
        pass


    def cliMsgReader(self):

        while True:
            msgObj = self.obj["msgServer"]

            for msgId in msgObj.inbox:
                if msgObj.inbox[msgId] in [True, False]:
                    print "Message id:%s , return: %s" % (msgId, msgObj.inbox[msgId])
                    del msgObj.outbox[msgId]
                self.doJob(msgObj.inbox[msgId])

                # [TODO] is any inbox message had time more than threshold, it must be removed.
        pass
