# this is a daemon process using multiprocess
import multiprocessing
import time
import sys
import logging

def daemon():
    while True:
        p = multiprocessing.current_process()
        logger.info("Info message")
        sys.stdout.flush()


def non_daemon():
    p = multiprocessing.current_process()
    print 'Starting:', p.name, p.pid
    sys.stdout.flush()
    print 'Exiting :', p.name, p.pid
    sys.stdout.flush()

if __name__ == '__main__':

    logger = logging.getLogger("DaemonLog")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.FileHandler("/Users/ajeetjha/zi/sqd/logs/testdaemon.log")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    d = multiprocessing.Process(name='daemon', target=daemon)
    d.daemon = True

    n = multiprocessing.Process(name='non-daemon', target=non_daemon)
    n.daemon = False

    d.start()
    time.sleep(1)
    n.start()