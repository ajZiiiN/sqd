
import logging
import time
import argparse
import sqdRunner as sqdR
from zmq_test.msgServer import msgServer
from zmq_test.msgClient import msgClient
import utils as u


def main():
    parser = argparse.ArgumentParser(description='Start Squirrel Daemon as Leader, Worker or Client...')


    parser.add_argument('--mode',nargs=2, choices=['client', 'leader', 'worker','sqd', 'start', 'stop', 'restart'],
                        help='sum the integers (default: find the max)')

    parser.add_argument('--status', choices=['full', 'mode'])

    args = parser.parse_args()

    cli = msgClient("172.16.0.166","6667")


    if args.mode != None:
        if args.mode[0] == "sqd":
            if args.mode[1]=="start":
                pass
        else:
            msg = u.createCliMsg("mode",(args.mode[0],args.mode[1]))
            print msg
            cli.send(msg)

    if args.status != None:
        msg = u.createCliMsg("status",(args.status,))
        print msg

    print "MODE: ", args.mode
    print "status: ", args.status

main()