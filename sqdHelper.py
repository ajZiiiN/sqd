

import utils
import os
import genMsgId as generator




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
        self.configFile = "configW.json"
        self.configDir = "/etc/sqd"
        self.baseConfigFile = "config.json"

        self.config = dict()
        self.workerConfig = dict()

        if utils.checkCreateDir (self.configDir):
            if not os.path.exists(os.path.join(self.configDir, self.configFile )) \
                    and not os.path.exists(os.path.join(self.configDir, self.baseConfigFile )) :
                self.createFromSample()
                print "Config created from sample..."
            else:
                print "Configs are messed up, please check and clean. "
                return

        if os.path.exists (os.path.join (self.configDir, self.configFile )):
            self.workerConfig = utils.readJSON(os.path.join (self.configDir, self.configFile ))
            print "Worker config updated..."

        if os.path.exists(os.path.join(self.configDir, self.baseConfigFile )):
            self.config = utils.readJSON(os.path.join(self.configDir, self.baseConfigFile))
            print "Base config updated..."

        pass

    def createFromSample(self):

        # [TODO] DO clean cluster start with only self as part of fresh cluster
        # for now on the fresh start we initialize using the sample config, which is created manually

        confL = utils.readJSON("config/configW_sample.json")
        utils.writeJSON(os.path.join(self.configDir, self.configFile), confL)

        conf = utils.readJSON("config/config_sample.json")
        utils.writeJSON(os.path.join(self.configDir, self.baseConfigFile), conf)


        pass

    def initWorker(self):
        # read the raw config (Created from sample)
        # clean worker/clients, worker/leader , worker/cluster, worker/game

        confType = self.leaderConfig["@name"]

        self.workerConfig[confType]["clients"] =[]
        self.workerConfig[confType]["leader"] = ""
        self.workerConfig[confType]["cluster"] = ""
        self.workerConfig[confType]["game"] = -1

        utils.writeJSON(os.path.join(self.configDir, self.configFile), self.workerConfig)
        print "Worker config had been modified..."
        pass

    def addToCluster (self, leaderIP):
        # asks leader to add itself to the cluster
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
        self.configFile = "configL.json"
        self.configDir = "/etc/sqd"
        self.baseConfigFile = "config.json"

        self.config = dict()
        self.leaderConfig = dict()

        if utils.checkCreateDir(self.configDir):
            if not os.path.exists(os.path.join(self.configDir, self.configFile )) \
                and not os.path.exists(os.path.join(self.configDir, self.baseConfigFile )) :
                self.createFromSample()
                print "Config created from sample..."
            else:
                print "Configs are messed up, please check and clean. "
                return

        if os.path.exists (os.path.join (self.configDir, self.configFile )):
            self.leaderConfig = utils.readJSON(os.path.join (self.configDir, self.configFile ))
            print "Leader config updated..."

        if os.path.exists(os.path.join(self.configDir, self.baseConfigFile )):
            self.config = utils.readJSON(os.path.join(self.configDir, self.baseConfigFile))
            print "Base config updated..."

        pass

    def createFromSample(self):

        # [TODO] DO clean cluster start with only self as part of fresh cluster
        # for now on the fresh start we initialize using the sample config, which is created manually

        confL = utils.readJSON("config/configL_sample.json")
        utils.writeJSON(os.path.join(self.configDir, self.configFile), confL)

        conf = utils.readJSON("config/config_sample.json")
        utils.writeJSON(os.path.join(self.configDir, self.baseConfigFile), conf)


        pass

    def initCluster(self):
        # given the list of node to start with, construct a cluster
        # cleans junk from config

        # cleans leader/clients , leader/relation, leader/workers, cluster
        confType = self.leaderConfig["@name"]
        self.leaderConfig[confType]["clients"] = []
        self.leaderConfig[confType]["relation"] = dict()
        self.leaderConfig[confType]["workers"] = []
        self.leaderConfig[confType]["cluster"] = ""

        # resets leader/workers with host
        host = self.leaderConfig[confType]["host"]
        self.leaderConfig[confType]["workers"].append(host)

        # resets cluster with new cluster ID
        clusterId = generator.genNewId()
        self.leaderConfig[confType]["cluster"] = clusterId

        utils.writeJSON(os.path.join(self.configDir, self.configFile), self.leaderConfig)

        print "Leader config had be changed..."
        pass

    def addClient(self, clientIP):
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



class sender:

    def __init__(self, daemon):
        # daemon is the class object, ie. sqdL, sqdW or sqdC
        self.daemon = daemon

    def initSender(self):





