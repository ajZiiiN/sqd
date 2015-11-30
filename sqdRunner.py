
import sqdHelper as sqdH


# start cluster/leader
# add worker
# add client

class sqdRunner:

    def __init__(self):
        #initialize process ID to stop while they are running
        self.leaders = []
        self.workers = []
        self.clients = []
        pass

    def startLeader(self):
        # get new sqdL object
        # init cluster if new
        # handle difference between new and and existing cluster
        # is config is new, initCluster

        # create msg client for each workers and send ask to each one of them
        # Create a message dictionary for response maintaining all messages currently being sent and waiting for ack
        # create
        pass

    def stopLeader(self):
        pass

    def restartLeader(self):
        pass

    def startWorker(self):
        pass

    def stopWorker(self):
        pass

    def restartWorker(self):
        pass


