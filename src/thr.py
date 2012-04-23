import thread
from util import cells_of_thread

def child_thread(q, thr_func) :
    while True :
        g_thr_index = q.get()
        print 'thread id : %s, g_thr_index : %s' % (thread.get_ident(), g_thr_index),

        map(thr_func, cells_of_thread(g_thr_index))
        print
        q.task_done()
