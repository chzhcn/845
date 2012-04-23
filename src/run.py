import os
import Queue
import threading
import thread

from multiprocessing import Pool, Process

from defines import *

from util import thr_indice, cells_of_thread

def print_func(cell) :
    print cell,

def child_thread(q, thr_func) :
    while True :
        g_thr_index = q.get()
        print 'thread id : %s, g_thr_index : %s' % (thread.get_ident(), g_thr_index),

        map(thr_func, cells_of_thread(g_thr_index))
        print
        q.task_done()

def child_process(index) :
    print 'pid: %s, index: %s' % (os.getpid(), index)

    q = Queue.Queue()

    [threading.Thread(target = child_thread, args = (q, print_func)).start() for i in xrange(num_thread_region)]

    while True :
        map(lambda thr_index : q.put(thr_index), thr_indice(index))
        q.join()
        print 'one iteration'

if __name__ == '__main__' :
    # print 'pid: %s' % os.getpid()
    p = Process(target = child_process, args=(31,))
    p.start()
    p.join()

    # pool = Pool(num_region)
    # pool.map_async(child_process, (x for x in xrange(num_region)))
    # pool.close()
    # pool.join()
