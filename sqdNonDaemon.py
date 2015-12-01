
import logging
import time
import argparse
import sqdRunner as sqdR
from zmq_test.msgServer import msgServer
from zmq_test.msgClient import msgClient
import utils as u

def main():

    runner = sqdR.sqdRunner()
    runner.obj["msgServer"] = msgServer("172.16.0.166","6667")

    runner.obj["msgServer"].run()

    #while True:
    #   time.sleep(20)

    for t in runner.obj["msgServer"].threads:
        t.join()

main()