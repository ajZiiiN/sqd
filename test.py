import os
import json
import thread
import time
import threading

from zmq_test.msgClient import msgClient
from zmq_test.msgServer import msgServer



threads= []
#threads.append(thread.start_new_thread(f,()))
#threads.append(thread.start_new_thread(g,()))

cli = msgClient("172.16.0.166")
ser = msgServer("172.16.0.166")

t1 = threading.Thread(target=cli.run, args=())
t1.start()
threads.append(t1)

t2 = threading.Thread(target=ser.run, args=())
t2.start()
threads.append(t2)


for i in range(1,20):
    cli.send("MSG-CLI" + str(i))
    time.sleep(1)
    ser.send("MSG-SER" + str(i))
    time.sleep(1)
'''
time.sleep(20)
cli.stop()

time.sleep(5)
ser.stop()

'''

for t in threads:
    t.join()