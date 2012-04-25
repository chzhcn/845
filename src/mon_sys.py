import sys
import os
import Queue
import threading
import thread
import random
import socket
import pickle

from defines import *
from multiprocessing import Pool, Process
from util import thr_indice, cells_of_thread, cells_of_region

data_path = None
result_map = {}

def print_cell(cell) :
    print cell,

def cell_result(res) :
    return 1 if sum(res) > success_threshold * len(res) else 0

def ping_cell(cell) :
    cell_path = data_path + os.sep + str(cell[0]) + '-' + str(cell[1])
    samples = {}
    with open(cell_path, 'r') as fcell:
        lines = fcell.readlines()
        size = len(lines)
        sample_size = size * sample_rate
        i = 0
        while i < sample_size :
            s = random.randint(0, size - 1)
            if s not in samples.keys() :
                # print lines[s][-2:-1]
                samples[s] = int(lines[s][-2:-1])
                i += 1
    res = samples.values()
    result = cell_result(res)
    if result == 0 :
        result_map[cell] = result

def child_thread(q, thr_func) :
    while True :
        g_thr_index = q.get()
        # print 'thread id : %s, g_thr_index : %s' % (thread.get_ident(), g_thr_index),

        map(thr_func, cells_of_thread(g_thr_index))
        # print
        q.task_done()

def mon_process(index) :
    print 'pid: %s, index: %s' % (os.getpid(), index)

    q = Queue.Queue()
    # result_map = {}

    # for cell in cells_of_region(index) : print cell

    # thr_worker = print_cell
    thr_worker = ping_cell
    [threading.Thread(target = child_thread, args = (q, thr_worker)).start() for i in xrange(num_thread_region)]

    while True :
        result_map.clear()
        map(lambda thr_index : q.put(thr_index), thr_indice(index))
        q.join()
        print result_map
        send_process_result(result_map)
        # print 'one iteration'
        # break

def send_process_result(map) :
    try :
        send_socket = socket.create_connection(report_addr, 10)
        data = pickle.dumps(map)
        send_socket.send(data);
    except Exception as inst:
        print type(inst)
        print inst
        print "send_process_result() exception. report_addr: %s obj: %s" % (report_addr, str(map))
        # raise

if __name__ == '__main__' :
    data_path = sys.argv[1]
    print 'pid: %s' % os.getpid()
    worker = mon_process
    
    p = Process(target = worker, args=(0, ))
    p.start()
    p.join()

    # [Process(target = worker, args = (i,)).start() for i in xrange(num_region)]

