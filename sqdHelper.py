






class sqdC:
    '''
    Client class for squirrel daemon.
    '''

    def __init__(self,  gameId):
        # Initializes squirrel daemon with necessary information
        # ---
        self.gameId = gameId
        # store in config

        pass

    def pollWorker(self):
        # Checks if Worker has been pulling data from the client or not
        # ---
        # get Worker ip from config
        # ping the worker IP, if alive return True else False
        pass

    def changeWorker(self):
        # changes worker
        # ---
        # Send Leader a message
        pass

    def tuneWorker(self):
        #ask worker to get data from client fast
        pass

    def getNewWorker(self):
        # Asks Leader for a new worker
        # confirms the worker
        pass

    def confirmWorker(self):
        # gets and stores information about the worker it is interacting with
        # keeps checking on worker if it is alive, if not notifies leader to get a new one
        # [NOTE] worker can reject client and in that case Client should ask leader for new worker.
        # post death, use the same method to confirm that the
        pass

    def iamClient(self, leaderIP):
        # adding to specific cluster
        # Sets class variable with clusterUID
        # get ack from leader, saves in config file
        pass



class sqdW:
    '''
    Worker class for squirrel daemon.
    '''

    def __init__(self):
        pass

    def addToCluster (self, leaderIP):
        # askes leader to add itself to the cluster
        pass

    def addClient(self):
        #collects clients from the leader.
        pass

    def confirmClient(self):
        # post death, confirm the clients it previously had.
        pass

    def ackClient(self):
        # handler for pollWorker, replying that the worker is alive
        pass

    def removeClient(self):
        # on changeWorker or when client is dead client info should be removed from the config
        pass

    def setTuningFromClient(self):
        # for each specific client, specify speed at which data should be taken
        pass

    def getDataFromClient(self):
        # keep pulling data from client at the rate set by client or leader
        pass

    def getInfoOnClientData(self):
        # get storage and rate from which we are getting data from a client
        # keep the config update
        pass


class sqdL:
    '''
    Leader class for squirrel daemon.
    '''

    def __init__(self):
        pass

    def initCluster(self):
        # given the list of node to start with, construct a cluster
        pass

    def addClient(self):
        # Setting up connection between a client and a Worker
        pass

    def addWorker(self):
        # adding worker to cluster
        pass

    def removeWorker(self):
        #remove worker from client and break its relation with all clients
        pass

    def removeClient(self):
        #remove client, breaad its relation with the worker
        pass






