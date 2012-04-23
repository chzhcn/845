import sys
import os
import Queue
import threading

from multiprocessing import Pool, Process

from defines import *

from util import thr_indice
from thr import child_thread

data_path = None

def print_cell(cell) :
    print cell,

def ping_cell(cell) :
    print data_path

def mon_process(index) :
    print 'pid: %s, index: %s' % (os.getpid(), index)

    q = Queue.Queue()

    thr_worker = ping_cell
    [threading.Thread(target = child_thread, args = (q, thr_worker)).start() for i in xrange(num_thread_region)]

    while True :
        map(lambda thr_index : q.put(thr_index), thr_indice(index))
        q.join()
        print 'one iteration'

if __name__ == '__main__' :
    data_path = sys.argv[1]
    # print 'pid: %s' % os.getpid()
    worker = mon_process
    p = Process(target = worker, args=(31,))
    p.start()
    p.join()

    # pool = Pool(num_region)
    # pool.map_async(worker, (x for x in xrange(num_region)))
    # pool.close()
    # pool.join()
