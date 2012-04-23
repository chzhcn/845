import os
import Queue
import threading
import thread

from multiprocessing import Pool, Process
from multiprocessing.pool import ThreadPool

from defines import *

from util import thr_indice
from util import cells_of_region
from util import cells_of_thread

def child_thread(q) :
    while True :
        g_thr_index = q.get()
        print 'thread id : %s, g_thr_index : %s' % (thread.get_ident(), g_thr_index)
        q.task_done()

def child_process(index) :
    print 'pid: %s, ppid: %s, index: %s' % (os.getpid(), os.getppid(), index)

    q = Queue.Queue()

    threads = [threading.Thread(target = child_thread, args = (q, )) for i in xrange(num_thread_region)]

    map(lambda thread : thread.start(), threads)

    while True :
        map(lambda thr_index : q.put(thr_index), thr_indice(index))
        q.join()
        print 'one iteration'
    
    # for cell in cells_of_region(index) :
    #     print cell
    

if __name__ == '__main__' :
    print 'pid: %s' % os.getpid()
    p = Process(target = child_process, args=(2,))
    p.start()
    p.join()
    
    # pool = Pool(num_region)
    # pool.map_async(child_process, (x for x in xrange(num_region)))
    # pool.close()
    # pool.join()
