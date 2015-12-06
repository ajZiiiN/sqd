

import utils
import os
import genMsgId as generator
from zmq_test.msgServer import msgServer
from zmq_test.msgClient import msgClient
import utils as u
import datetime
import time
import threading



class sqdC:
    '''
    Client class for squirrel daemon.
    '''

    def __init__(self):
        # Initializes squirrel daemon with necessary information
        # ---
        self.gameId = -1
        # store in config

        self.configFile = "configC.json"
        self.configDir = "/etc/sqd"
        self.baseConfigFile = "config.json"

        self.config = dict()
        self.clientConfig = dict()
        self.msgObj = None # This is msgServer, initialized when we start the worker

        self.jobMap = {
            "iamClient" : self.iamClient
        }

        if utils.checkCreateDir (self.configDir):
            if not os.path.exists(os.path.join(self.configDir, self.configFile )) \
                    and not os.path.exists(os.path.join(self.configDir, self.baseConfigFile )) :
                self.createFromSample("all")
                print "Config created from sample..."
            else:
                print "Configs are messed up, please check and clean. "


        if os.path.exists (os.path.join (self.configDir, self.configFile )):
            self.clientConfig = utils.readJSON(os.path.join (self.configDir, self.configFile ))
            print "Client config updated..."
        else:
            self.createFromSample("client")
            self.clientConfig = utils.readJSON(os.path.join (self.configDir, self.configFile ))
            print "Client config updated from sample..."

        if os.path.exists(os.path.join(self.configDir, self.baseConfigFile )):
            self.config = utils.readJSON(os.path.join(self.configDir, self.baseConfigFile))
            print "Base config updated..."
        else:
            self.createFromSample("main")
            self.config = utils.readJSON(os.path.join(self.configDir, self.baseConfigFile))
            print "Base config updated from sample...."

        pass

    def createFromSample(self, type):

        # [TODO] DO clean cluster start with only self as part of fresh cluster
        # for now on the fresh start we initialize using the sample config, which is created manually

        if(type == "client" or type =="all"):
            confC = utils.readJSON("config/configC_sample.json")
            utils.writeJSON(os.path.join(self.configDir, self.configFile), confC)

        if(type == "main" or type =="all"):
            conf = utils.readJSON("config/config_sample.json")
            utils.writeJSON(os.path.join(self.configDir, self.baseConfigFile), conf)


        pass

    def initClient(self):
        # read the raw config (Created from sample)
        # clean client/leader, client/worker , client/cluster

        confType = self.clientConfig["@name"]

        self.clientConfig[confType]["leader"] =""
        self.clientConfig[confType]["worker"] = ""
        self.clientConfig[confType]["cluster"] = ""
        self.clientConfig[confType]["game"] = -1
        self.clientConfig[confType]["new"] = False

        utils.writeJSON(os.path.join(self.configDir, self.configFile), self.clientConfig)
        print "Client config had been modified..."
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

    def iamClient(self, id, args):
        # adding to specific cluster
        # handler for add client, message details
        # gets details from Leader and sets all details
        # sends an ack message with gameID, username(default moonfrog), fromPath
        # --
        print "I am the Client..."
        self.clientConfig["client"]["leader"] = args[0]
        self.clientConfig["client"]["cluster"] = args[1]
        self.clientConfig["client"]["worker"] = args[2]

        utils.writeJSON(os.path.join(self.configDir, self.configFile), self.clientConfig)
        print "Updating Client config..."

        print "I am alive..."

        msgId = id
        type = "A"
        sName = "sqdC/iamClient"
        rName = "sqdL"
        now = datetime.datetime.now()
        opName = "addClient"

        args = (self.clientConfig["client"]["host"], self.clientConfig["client"]["game"], self.clientConfig["client"]["frompath"] )

        msg = u.createMsg(msgId, type, sName, rName, now, opName, args)

        self.msgObj.send(msg)
        self.msgObj.inbox.pop(id,0)



        # Sets class variable with clusterUID


        pass

    def doJob(self, id, msgD):
        # for this message do something
        print "doing job for: ", str(msgD)

        print str(self.jobMap[msgD["opName"]])
        self.jobMap[msgD["opName"]](id, msgD["args"])


        pass

    def msgReader(self):
        print "Reading already..."
        while True:
            ids = self.msgObj.inbox.keys()
            for msgId in ids:
                if self.msgObj.inbox[msgId]["type"] == "R":
                    self.doJob(msgId, self.msgObj.inbox[msgId])

                    # [TODO] is any inbox message had time more than threshold, it must be removed.
        pass

    def reader(self):
        print "Reader for worker..."
        t = threading.Thread(target=self.msgReader)
        t.daemon = True
        t.start()



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
        self.msgObj = None # This is msgServer, initialized when we start the worker

        self.jobMap = {
            "addToCluster" : self.addToCluster,
            "iamAlive" : self.iamAlive,
            "addClient": self.addClient
        }

        if utils.checkCreateDir (self.configDir):
            if not os.path.exists(os.path.join(self.configDir, self.configFile )) \
                    and not os.path.exists(os.path.join(self.configDir, self.baseConfigFile )) :
                self.createFromSample("all")
                print "Config created from sample..."
            else:
                print "Configs are messed up, please check and clean. "


        if os.path.exists (os.path.join (self.configDir, self.configFile )):
            self.workerConfig = utils.readJSON(os.path.join (self.configDir, self.configFile ))
            print "Worker config updated..."
        else:
            self.createFromSample("worker")
            self.workerConfig = utils.readJSON(os.path.join (self.configDir, self.configFile ))
            print "Worker config updated from sample..."

        if os.path.exists(os.path.join(self.configDir, self.baseConfigFile )):
            self.config = utils.readJSON(os.path.join(self.configDir, self.baseConfigFile))
            print "Base config updated..."
        else:
            self.createFromSample("main")
            self.config = utils.readJSON(os.path.join(self.configDir, self.baseConfigFile))
            print "Base config updated from sample...."

        pass

    def createFromSample(self, type):

        # [TODO] DO clean cluster start with only self as part of fresh cluster
        # for now on the fresh start we initialize using the sample config, which is created manually

        if(type == "worker" or type =="all"):
            confL = utils.readJSON("config/configW_sample.json")
            utils.writeJSON(os.path.join(self.configDir, self.configFile), confL)

        if(type == "main" or type =="all"):
            conf = utils.readJSON("config/config_sample.json")
            utils.writeJSON(os.path.join(self.configDir, self.baseConfigFile), conf)


        pass

    def initWorker(self):
        # read the raw config (Created from sample)
        # clean worker/clients, worker/leader , worker/cluster, worker/game

        confType = self.workerConfig["@name"]

        self.workerConfig[confType]["clients"] =[]
        self.workerConfig[confType]["leader"] = ""
        self.workerConfig[confType]["cluster"] = ""
        self.workerConfig[confType]["game"] = -1
        self.workerConfig[confType]["new"] = False

        utils.writeJSON(os.path.join(self.configDir, self.configFile), self.workerConfig)
        print "Worker config had been modified..."
        pass

    def addToCluster (self, leaderIP):

        # asks leader to add itself to the cluster

        pass

    def addClient(self, id, args ): # find arguments in args of msgbox
        # collects a client from the leader.
        # Needs some client configs: gameID, fromPath
        # start a subprocess to keep syncing data, for now lets start thread
        #msgD = self.msgObj.inbox[id]
        clientIP = args[0]
        gameID = args[1]
        fromPath = args[2]

        self.workerConfig["worker"]["clients"].append(clientIP)
        utils.writeJSON(os.path.join(self.configDir, self.configFile), self.workerConfig)

        # [TODO]  in case start cluster but not new, for each client IP who does not have process to get data, start them
        # start rsync job for all this client
        print "starting Rsync for ip: %s , gameID: %s , fromPath: %s " % ( clientIP, gameID, fromPath)

        print "I am alive..."
        msg = u.createAckMsg(id,1)

        self.msgObj.send(msg)
        self.msgObj.inbox.pop(id,0)
        return

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

    def iamAlive(self, id, args=None):
        print "I am alive..."
        msg = u.createAckMsg(id,1)

        self.msgObj.send(msg)
        self.msgObj.inbox.pop(id,0)
        return




    def doJob(self, id, msgD):
        # for this message do something
        print "doing job for: ", str(msgD)

        print str(self.jobMap[msgD["opName"]])
        self.jobMap[msgD["opName"]](id, msgD["args"])


        pass

    def msgReader(self):
        print "Reading already..."
        while True:
            ids = self.msgObj.inbox.keys()
            for msgId in ids:
                if self.msgObj.inbox[msgId]["type"] == "R":
                    self.doJob(msgId, self.msgObj.inbox[msgId])

                # [TODO] is any inbox message had time more than threshold, it must be removed.
        pass

    def reader(self):
        print "Reader for worker..."
        t = threading.Thread(target=self.msgReader)
        t.daemon = True
        t.start()


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
        self.workers = dict() # mapping between ip and msgObject || each message object has inbox
        self.clients = dict() # mapping between ip and msgObject || each message object has inbox

        self.job_functions = {
            "worker": {
                "add": self.addWorker,
                "remove" : self.removeWorker
            },
            "client": {
                "add": self.addClient,
                "remove" : self.removeClient

            }
        }

        # checking config directory
        if utils.checkCreateDir(self.configDir):
            if not os.path.exists(os.path.join(self.configDir, self.configFile )) \
                and not os.path.exists(os.path.join(self.configDir, self.baseConfigFile )) :
                self.createFromSample("all")
                print "Config created from sample..."
            else:
                print "Configs are messed up, please check and clean. "

        if os.path.exists (os.path.join (self.configDir, self.configFile )):
            self.leaderConfig = utils.readJSON(os.path.join (self.configDir, self.configFile ))
            print "Leader config updated..."
        else:
            self.createFromSample("leader")
            self.leaderConfig = utils.readJSON(os.path.join (self.configDir, self.configFile ))
            print "Leader config updated..."


        if os.path.exists(os.path.join(self.configDir, self.baseConfigFile )):
            self.config = utils.readJSON(os.path.join(self.configDir, self.baseConfigFile))
            print "Base config updated..."
        else:
            self.createFromSample("main")
            self.config = utils.readJSON(os.path.join(self.configDir, self.baseConfigFile))
            print "Base config updated..."

        # [TODO] start messengers for each worker and clients available.

        pass

    def createFromSample(self, type):

        # [TODO] DO clean cluster start with only self as part of fresh cluster
        # for now on the fresh start we initialize using the sample config, which is created manually
        if(type == "leader" or type =="all"):
            confL = utils.readJSON("config/configL_sample.json")
            utils.writeJSON(os.path.join(self.configDir, self.configFile), confL)

        if(type == "main" or type =="all"):
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
        self.leaderConfig[confType]["idle_workers"] = []
        self.leaderConfig[confType]["new"] = False

        # resets leader/workers with host
        host = self.leaderConfig[confType]["host"]
        self.leaderConfig[confType]["workers"].append(host)

        # resets cluster with new cluster ID
        clusterId = generator.genNewId()
        self.leaderConfig[confType]["cluster"] = clusterId

        utils.writeJSON(os.path.join(self.configDir, self.configFile), self.leaderConfig)

        print "Leader config had be changed..."
        pass


    def addWorker(self, ip):
        # adding worker to cluster
        # ---
        print "Adding worker: " + ip
        existingWorkersInConfig = self.leaderConfig["leader"]["workers"]

        if ip not in existingWorkersInConfig:
            self.leaderConfig["leader"]["workers"].append(ip)
            #update config
            utils.writeJSON(os.path.join(self.configDir, self.configFile), self.leaderConfig)

        existingWorkersInServer = self.workers.keys()

        if ip not in existingWorkersInServer:
            print "Starting new msgClient for: ", ip
            self.workers[ip] = msgClient(ip)
            self.workers[ip].run()
        # Response handler for new worker coming in
        # If workers name
        print "checking worker: ", ip
        ret = self.checkWorker(ip)
        print "Found: ", str(ret)
        pass

    def addClient(self, ip):
        # adding client to cluster
        # ---
        print "Adding client: " + ip
        existingClientsInConfig = self.leaderConfig["leader"]["clients"]

        if ip not in existingClientsInConfig:
            self.leaderConfig["leader"]["clients"].append(ip)
            #update config
            utils.writeJSON(os.path.join(self.configDir, self.configFile), self.leaderConfig)

        existingClientsInServer = self.clients.keys()

        if ip not in existingClientsInServer:
            self.clients[ip] = msgClient(ip)
            self.clients[ip].run()

        # Check for client
        print "Checking Client..."
        ret = None
        msgId = u.genNewId()
        type = "R"
        sName = "sqdL/addClient"
        rName = "sqdC"
        now = datetime.datetime.now()
        opName = "iamClient"

        # [TODO] for now always the last worker ip is send for testing purposes.
        # it should be same worker on which addClient is envoked after getting infor from client
        workerIp =  self.leaderConfig["leader"]["workers"][-1]
        args = (self.leaderConfig["leader"]["host"], self.leaderConfig["leader"]["cluster"], workerIp)

        msg = u.createMsg(msgId, type, sName, rName, now, opName, args)


        if ip not in self.clients.keys():
            print "Client (%s) not available..." % (ip,)
        else:
            id, M = u.resolveMsg(msg)
            self.clients[ip].outbox[id] = M

            self.clients[ip].send(msg)
            print "checkClient: " + msg

            for i in range(1,40):
                if id  in self.clients[ip].inbox.keys():
                    ret = self.clients[ip].inbox[id]
                    self.clients[ip].inbox.pop(id,0)
                    self.clients[ip].outbox.pop(id,0)
                    print "Info from Client..", str(ret["args"])
                    break
                else:
                    time.sleep(2)

            # if got the necessary info from client
            # pass it on to worker
            if ret != None and len(ret["args"]) == 3:
                argsToWorker = ret["args"]
                ret = None

                idW = u.genNewId()
                type = "R"
                sName = "sqdL/addClient"
                rName = "sqdW"
                now = datetime.datetime.now()
                opName = "addClient"


                msg = u.createMsg(idW, type, sName, rName, now, opName, argsToWorker)

                print "keeping the message content in outbox..."
                curId, M = u.resolveMsg(msg)
                self.workers[workerIp].outbox[id] = M

                self.workers[workerIp].send(msg)
                print "Sending back to worker : ", msg

                for i in range(1,30):
                    if id  in self.workers[workerIp].inbox.keys():
                        ret = self.workers[workerIp].inbox[id]
                        self.workers[workerIp].inbox.pop(id,0)
                        self.workers[workerIp].outbox.pop(id,0)
                        return ret
                    else:
                        time.sleep(2)
            else:
                print "Something went wrong while sending to worker..."

        return ret

        # Response handler for new worker coming in
        # If workers name
        pass

    def removeWorker(self):
        #remove worker from client and break its relation with all clients
        pass

    def removeClient(self):
        #remove client, breaad its relation with the worker
        pass

    def checkWorker(self, ip):
        # assumes that msgClient at Leader has already started
        # --
        # createMsg(id, type, sName, rName, time, opName, args):
        #68926bc9cb24244f919aa03a090aa535::R::sqdC/Fname::sqdL::2015-12-02 00:02:30::addClient:<Args>
        print "Checking Worker..."
        ret = False
        msgId = u.genNewId()
        type = "R"
        sName = "sqdL/checkWorker"
        rName = "sqdW"
        now = datetime.datetime.now()
        opName = "iamAlive"
        args = tuple()

        msg = u.createMsg(msgId, type, sName, rName, now, opName, args)

        # send a message to Worker through msgClient
        if ip not in self.workers.keys():
            print "worker not available..."
        else:
            id, M = u.resolveMsg(msg)
            self.workers[ip].outbox[id] = M

            self.workers[ip].send(msg)
            print "checkWorker: " + msg

            for i in range(1,30):
                if id  in self.workers[ip].inbox.keys():
                    ret = self.workers[ip].inbox[id]
                    self.workers[ip].inbox.pop(id,0)
                    self.workers[ip].outbox.pop(id,0)
                    return ret
                else:
                    time.sleep(2)

        return ret


        # if send is success, its good
        # wait on its inbox to get an ack

        # Return True on Success and False on failure
        # its a blocking call

        pass


    def doJob(self, msgD):
        # for this message do something
        print "Leader doing job for: ", str(msgD)


        # the msg is a dictionary
        # return True if success else False

        # if job is done perfectly or inperfectly, log and delete object
        # return True or False as object

        pass

    def msgReader(self):

        while True:
            workers = self.workers.keys()
            for worker in workers:
                msgObj = self.workers[worker]

                # [TODO] there is a race with ack handelere who delete messages and readers who read them.
                # Solution: handel key errors
                ids = msgObj.inbox.keys()
                for msgId in ids:
                    if type(msgObj.inbox[msgId]) is not int and msgObj.inbox[msgId]["type"] == "R":
                        self.doJob(msgObj.inbox[msgId])

            # [TODO] is any inbox message had time more than threshold, it must be removed.
        pass

    # reader for Leader is totally different, it had to read across all messages in inbox of each of clients and workers
    def reader(self):
        t = threading.Thread(target=self.msgReader)
        t.daemon = True
        t.start()










