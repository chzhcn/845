from defines import *
import os # os.linesep
import random
import re
import threading
import Queue
from multiprocessing import Process, Pipe, Array
from mon_sys import child_thread
from util import thr_indice, region_grids_with_corner_indice, cell_to_region

prob_matrix = list()
pipes = list()
process_workers = list()
subproc_matrix = list()

def initialize():
    for i in range (0, num_cell_y):
        aRow = []
        for j in range (0, num_cell_x):
            aRow.append(normal_prob)
        sharedRow = Array('d', aRow)
        prob_matrix.append(sharedRow)  

def fill_matrix(prob, start_row = 0, end_row = num_cell_y, start_col = 0, end_col = num_cell_x):
    # check boundary
    if start_row < 0 or end_row > num_cell_y or start_col < 0 or end_col > num_cell_x:
        print "ERROR: Given boundary is wrong!"
        print "row range: (0, " + str(num_cell_y-1) + ") column range: (0, " + str(num_cell_x-1) + ")"
        return  
    
    for i in range (start_row, end_row):
        for j in range (start_col, end_col):
            prob_matrix[i][j] = prob

def print_usage():
    print "--------------------Usage of the disaster controller--------------------"
    print "Type 1: All servers are up. Input:1"
    print "Type 2: All servers are down. Input:2 "
    print "Type 3: Given a list of cells are down. Input:3 row1,col1 row2,col2 ..."
    print "Type 4: Let a rectangle region of cells down. Input:4 row1,col1 row2,col2"
    print "Type 5: All servers are up with a given probability. Input:5 probability"
    print "-----------------------------------------------------------------------"
            
def start_ui():
    print_usage()
    while True:
        rawInput = raw_input("Please input control parameter:")
            
        paraList = rawInput.split(" ")
        ctype = paraList[0]
        change_region = set()
        
        if ctype == '1':
            print "Type " + ctype + ": All servers are up."
            fill_matrix(1)
            change_region.update({x for x in range(num_region)})
            
        elif ctype == '2':
            print "type " + ctype + ": All servers are down."
            fill_matrix(0)
            change_region.update({x for x in range(num_region)})
            
        elif ctype == '3':
            print "type " + ctype + ": the given list of cells are down."
            for i in range(len(paraList)):
                if i != 0:
                    # the coordinate format is row,col
                    # if the format is (row,col), change r'\d+' to r'(\d+)'
                    row,col = map(int, re.findall(r'\d+', paraList[i]))
                    prob_matrix[row][col] = 0  
                    region_index = cell_to_region((row,col))
                    change_region.add(region_index)                            
            
        elif ctype == '4':
            print "type " + ctype + ": the rectangle region of cells are down."
            start_row, start_col = map(int, re.findall(r'\d+', paraList[1]))
            end_row, end_col = map(int, re.findall(r'\d+', paraList[2]))
            
            if start_row > end_row:
                start_row, end_row = end_row, start_row # swap
            
            if start_col > end_col:
                start_col, end_col = end_col, start_col # swap
                    
            fill_matrix(0, start_row, end_row+1, start_col, end_col+1)
            
            left_top_region = cell_to_region((start_row,start_col))
            right_down_region = cell_to_region((end_row,end_col))
            # this is a generator!
            for i in region_grids_with_corner_indice(left_top_region, right_down_region):
                change_region.add(i)
                        
        elif ctype == '5':
            prob = float(paraList[1])
            print "type " + ctype + ": All servers are up with " + str(prob*100) + "% probability."
            fill_matrix(prob) 
            change_region.update({x for x in range(num_region)})
              
        else:
            print "ERROR: Wrong control parameter!"
            continue
        #print_matrix()
        assign_jobs(change_region)
        
def start_controller():
    #initialize_worker_processes
    pipe_pairs = [Pipe() for x in range(num_region)]
    process_workers.extend([Process(target = control_process, args = (i, pipe_pairs[i][1], prob_matrix)) for i in xrange(num_region)])
    pipes.extend([pipe_pair[0] for pipe_pair in pipe_pairs])
    map(lambda p:p.start(), process_workers)

    start_ui()


    # worker_pool = Pool(processes=num_region)
    # worker_pool.map_async(control_process, (x for x in xrange(num_region)))
    # pool.map_async(worker, (x for x in xrange(num_region)))
    # pool.close()
    # pool.join()

def test_proc( index, pipe_conn):
    print "In test_proc:" + str(index),
    msg = pipe_conn.recv()
    print "   " + msg

    
# Generate processes (#: num_region_x * num_region_y)
# Each process generates threads (#: num_thread_region_x * num_thread_region_y)
# to do the job (write 1/0 to files) 
def assign_jobs(change_region):
    for i in change_region:
        print "aj:" + str(i)
        pipes[i].send("Go!")
    for i in change_region:
        msg = pipes[i].recv()
        print msg
     
def control_process( region_index, pipe_conn, shared_matrix):
    
    #print 'pid: %s, index: %s' % (os.getpid(), region_index)
   
    global subproc_matrix
    subproc_matrix = shared_matrix
    
    #print_matrix(subproc_matrix)
    
    q = Queue.Queue()

    [threading.Thread(target = child_thread, args = (q, do_control_job)).start() for i in xrange(num_thread_region)]
    
    while True :
        msg = pipe_conn.recv() #wait for signal from pipe

        #print "Worker process: " + str(region_index) + " "+ msg

        map(lambda thr_index : q.put(thr_index), thr_indice(region_index))
        q.join()
        #print "Worker process: " + str(region_index) + " Done!"
        pipe_conn.send("Worker process: " + str(region_index) + " Done!")

def do_test_job(cell):
    with open("doTestJob.txt", "w") as f:
        f.write(cell)
                        
def do_control_job(cell):
    #print "do_control_job for cell: " + str(cell)
    if cell == -1: #testing
        prob = prob_matrix[0][0]
        lines = []

        with open("0-0", "r") as f:
            for aLine in f.readlines():
                upOrDown = randUpOrDown(prob) 
                aLine = aLine.split(" ") # split for only getting IP
                #strip() to remove newline
                newLine = aLine[0].strip() + " " + str(upOrDown) + os.linesep
                #print newLine
                print repr(newLine)
                lines.append(newLine)
                #lines.append(aLine)
        with open("0-0", "w") as f:    
            f.writelines(lines)
    else: # x,y = cell
        row,col = cell
        prob = subproc_matrix[row][col]
        
        lines = [] 
        filename = os.path.abspath(str(row)+"-"+str(col))       
        #print "Processing " + filename
        with open(filename, "r") as f:
            for aLine in f.readlines():
                upOrDown = randUpOrDown(prob) 
                aLine = aLine.split(" ") # split for only getting IP
                #strip() to remove newline
                newLine = aLine[0].strip() + " " + str(upOrDown) + os.linesep
                #print repr(newLine)
                lines.append(newLine)
        with open(filename, "w") as f:    
            f.writelines(lines)
        
# given probability, return 0 (server down) or 1 (server up)
def randUpOrDown( prob):
    rand_num = random.random()
    if rand_num > prob:
        return 0
    else:
        return 1

def print_matrix(m = prob_matrix):
    for i in range (0, num_cell_y):
        for j in range (0, num_cell_x):
            print str(m[i][j]) + "\t",
        print  
    print "Size of matrix: (" + str(len(m)) + "," + str(len(m[0])) + ")"

if __name__ == '__main__' :
    initialize()
    print_matrix(prob_matrix)
    start_controller()


    