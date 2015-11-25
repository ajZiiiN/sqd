import os
import json

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
            print "Client sample config file not Found"
            return None

    if configType == "W":
        try:
            fd = open("config/configW_sample.json")
            return fd
        except IOError:
            print "Client sample config file not Found"
            return None