
import json
import os
import logging
import md5
from datetime import datetime
import subprocess

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

def genNewId():
    seed = datetime.now()
    id = md5.new(str(seed))

    return id.hexdigest()

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
    elif resolveAckMsg(msg) != None:
        return resolveAckMsg(msg)
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

def resolveAckMsg(msg):
    components = msg.split("::")

    if len(components) == 3:

        id = components[0]

        status = int(components[2])

        return (id,status)
    else:
        return None



def createCliMsg(op,args):
    msg = "CLI::"
    msg+= str(op) + "::" + str(args)

    return msg

# ack messages are of type id::A::[0,1] || 0 for failure 1 for success
def createAckMsg(id, value):
    msg = id + "::A::" + str(value)
    return msg

def fileTransfer(fromIp, pemKeyPath, fromPath, toPath):

    #rsync command
    # rsync --dry-run --remove-source-files -azv "ssh -i ~/.ssh/id_rsa" <source-ip>:~/home/ajha/testDir/* /Users/ajeetjha/zi/sqd/data/
    # Dry run cmd:- rsync -chavzP -e "ssh -i ~/.ssh/id_rsa" --dry-run --remove-source-files --stats  moonfrog@192.168.56.103:/home/moonfrog/sandbox/data/* /home/moonfrog/sandbox/data/
    # rsync -chavzP --stats moonfrog@192.168.56.102:/home/moonfrog/sandbox/data/* /home/moonfrog/sandbox/data/
    # Working cmd: rsync -chavzP -e "ssh -o "StrictHostKeyChecking no" -i ~/.ssh/id_rsa" --remove-source-files --stats  moonfrog@192.168.56.103:/home/moonfrog/sandbox/data/* /home/moonfrog/sandbox/data/

    rsyncCmdDry = 'rsync -chavzP -e "ssh -i ' + pemKeyPath + '" --remove-source-files --stats  moonfrog@' + \
        fromIp + ':' + fromPath + ' ' + toPath

    rsyncCmd = 'rsync -chavzP -e "ssh -i ' + pemKeyPath + '" --dry-run --remove-source-files --stats  moonfrog@' + \
                  fromIp + ':' + fromPath + ' ' + toPath

    p = subprocess.Popen(rsyncCmdDry, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    M = dict()
    M["count"] = 0
    M["bytes"] = 0
    outl = out.split("\n")
    for line in outl:
        if "Number of regular files transferred" in line:
            contents = line.split(" ")
            M["count"] += int(contents[-1])

        if "Total file size:" in line:
            contents = line.split(" ")
            if 'K' in contents[3]:
                M["bytes"] += float(contents[3][0:-1]) * 1000
            elif 'M' in contents[3]:
                M["bytes"] += float(contents[3][0:-1]) * 1000000
            elif 'G' in contents[3]:
                M["bytes"] += float(contents[3][0:-1]) * 1000000000
            else:
                M["bytes"] += float(contents[3])

    print "Executing: " ,rsyncCmd
    print "__________________________________"
    print out
    # Use stats to create the status info
    return M

    pass

def getLogger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fileHandler = logging.FileHandler(log_file)
    fileHandler.setFormatter(formatter)


    l.setLevel(level)
    l.addHandler(fileHandler)

    return l

def getHost():
    cmd = "ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    host =  out.strip()
    return host


def setupSample():
    #client
    cl = readJSON("config/configC_sample.json")
    wo = readJSON("config/configW_sample.json")
    le = readJSON("config/configL_sample.json")

    host = getHost()

    cl["host"] = host
    wo["host"] = host
    le["host"] = host

    writeJSON("config/configC_sample.json", cl)
    writeJSON("config/configW_sample.json", wo)
    writeJSON("config/configL_sample.json", le)


