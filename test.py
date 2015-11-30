import os
import json
import thread
import time
import threading

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

t1 = threading.Thread(target=f)
t1.start()
threads.append(t1)

t2 = threading.Thread(target=g)
t2.start()
threads.append(t2)

for t in threads:
    t.join()