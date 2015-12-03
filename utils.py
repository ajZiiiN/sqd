
import json
import os

def checkCreateDir(path):

    if os.path.exists(path) and os.path.isdir(path):
        return True
    else:
        try:
            os.makedirs(path)
            return True
        except OSError as e:
            print e
            return False


def checkCreateFile(path, fileName):

    filePath = os.path.join(path, fileName)
    if os.path.exists(filePath):
        print "Can not create, file exists: " + filePath

    elif (not os.path.exists(path)) or (not os.path.isdir(path)) :
        print "Check parent path: " + path

    elif os.path.exists(path) and os.path.isdir(path):
        try:
            open(filePath,"w+")
            return True
        except IOError as e:
            print e
            return False
    return False

def writeJSON(filePath, conf):

    with open(filePath,"w") as f:
        f.truncate()
        json.dump(conf,f, indent=2, sort_keys=True)
        f.flush()

def readJSON(filePath):

    with open(filePath , "r") as f:
        ret = json.loads(f.read())

    return ret

def checkSampleConfig(configType):
    if configType == "C":
        try:
            fd = open("config/configC_sample.json")
            return fd
        except IOError:
            print "Client sample config file not Found"
            return None

    if configType == "L":
        try:
            fd = open("config/configL_sample.json")
            return fd
        except IOError:
            print "Leader sample config file not Found"
            return None

    if configType == "W":
        try:
            fd = open("config/configW_sample.json")
            return fd
        except IOError:
            print "Worker sample config file not Found"
            return None

def createConfigC() :

    # Create a base config which sets

    # check if src/config/configC.sample is present
    # Create a new config at /etc/sqd/configL.json
    pass

def convertIpToDir(ip):
    return ip.replace(".","-")

def resolveMsg(msg):


    if resolveCliMsg(msg) != None:
        return resolveCliMsg(msg)
    else:
        M = dict()
        components = msg.split('::')
        id = components[0]
        M["type"] = components[1]
        M["sName"] = components[2]
        M["rName"] = components[3]
        M["time"] = components[4]
        M["opName"] = components[5]

        if components[6][0] == '(' and components[6][-1] == ')':
            M["args"] = eval(components[6])
        else:
            print "Arguments not a tuple..."
            M[args] = tuple()

        return (id,M)

    # [TODO] except array out of index error

def createMsg(id, type, sName, rName, time, opName, args):
    msg = str(id)
    msg += "::" + str(type) + "::" + str(sName) + "::" + str(rName)
    msg += "::" + str(time) + "::" + str(opName) + "::" + str(args)

    return msg

def resolveCliMsg(msg):

    components = msg.split("::")
    if components[0] == "CLI":
        M = dict()
        M['op'] = components[1]
        M['args'] = tuple()

        if components[2][0] == '(' and components[2][-1] == ')':
            M['args'] = eval(components[2])
        return "CLI", M
    else:
        return None

def createCliMsg(op,args):
    msg = "CLI::"
    msg+= str(op) + "::" + str(args)

    return msg

def setSampleConfig():
    pass