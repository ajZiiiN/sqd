
import logging
import time
import argparse
import sqdRunner as sqdR
from zmq_test.msgServer import msgServer
from zmq_test.msgClient import msgClient
import utils as u
import threading


def main():


    runner = sqdR.sqdRunner()
    runner.startMsgServer("192.168.56.1","6667")

    runner.obj["msgServer"].run()

    #while True:
    #   time.sleep(20)

    t = threading.Thread(target=runner.cliMsgReader)
    t.daemon = True
    t.start()

    # t.join()

    for t in runner.obj["msgServer"].threads:
        t.join()




main()