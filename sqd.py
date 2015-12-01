
'''

This is the main daemon which acts as Leader, Client and Worker.

Few workers and one Leader forms a cluster.

Each sqd-W is started with a worker argument.
Further, on Leader not this worker must be added, with command add worker.

Each sqd-C is starte with a client argument.
Further, on leader node this Client must be added.

Each sqd-L is started with a leader argument.
It can be initialized with set of clients and workers.

'''


#standard python libs
import logging
import time
import argparse
import sqdRunner as sqdR
from zmq_test.msgServer import msgServer
from zmq_test.msgClient import msgClient
import utils as u



#third party libs
from daemon import runner


class App:

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path =  '/Users/ajeetjha/zi/sqd/samples/sqdL.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            # Main code goes here ...


            # get localhost msgServer
            # start handelling cli messages [cli message reader]



            logger.debug("Debug message")
            logger.info("Info message")
            logger.warn("Warning message")
            logger.error("Error message")
            time.sleep(10)


app = App()

logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/Users/ajeetjha/zi/sqd/logs/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()



