import os
import json
import thread
import time
import threading

from zmq_test.msgClient import msgClient
from zmq_test.msgServer import msgServer



def f():
    for i in range(1,20):
        print "Yo..."
        print f.__myname__
        time.sleep(2)


def g():
    for i in range(1,5):
        print "Go..."
        time.sleep(3)

threads= []
#threads.append(thread.start_new_thread(f,()))
#threads.append(thread.start_new_thread(g,()))

cli  = msgClient("172.16.0.166")
ser = msgServer("172.16.0.166")

t1 = threading.Thread(target=cli.run, args=())
t1.start()
threads.append(t1)

t2 = threading.Thread(target=ser.run, args=())
t2.start()
threads.append(t2)

'''
time.sleep(20)
cli.stop()

time.sleep(5)
ser.stop()

'''

for t in threads:
    t.join()