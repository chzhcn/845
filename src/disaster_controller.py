from defines import *
import os # os.linesep
import random
import re
import threading
import thread
import Queue
from multiprocessing import Pool, Process, Pipe
from thr import child_thread
from util import thr_indice

'''
self.thread_stream = threading.Thread(target=self.stream_music, args=(message,))
339 self.thread_stream.start()
def stream_music(self, message) :
'''

class disaster_controller:
    normal_prob = 0.95
    # size of matrix is the same as the map
    # each element's value is the probability of disaster NOT happening
    prob_matrix = None
    pipes = None
    process_workers = None
    def __init__(self):
        self.prob_matrix = []
        for i in range (0, num_cell_y):
            aRow = []
            for j in range (0, num_cell_x):
                aRow.append(self.normal_prob)
            self.prob_matrix.append(aRow)  
        self.initialize_worker_processes()
    
    def fill_matrix(self, prob, start_row = 0, end_row = num_cell_y, start_col = 0, end_col = num_cell_x):
        # check boundary
        if start_row < 0 or end_row > num_cell_y or start_col < 0 or end_col > num_cell_x:
            print "ERROR: Given boundary is wrong!"
            print "row range: (0, " + str(num_cell_y-1) + ") column range: (0, " + str(num_cell_x-1) + ")"
            return  
        
        for i in range (start_row, end_row):
            for j in range (start_col, end_col):
                self.prob_matrix[i][j] = prob
    
    def cell_to_region(self, cell):
        row,col = cell
        reg_row = row / cell_per_region_y
        reg_col = col / cell_per_region_x
        region_index = reg_row*num_region_x + reg_col
        return region_index
    
    def region_index_to_grid(self, index):
        
        pass
    
    
    def print_usage(self):
        print "--------------------Usage of the disaster controller--------------------"
        print "Type 1: All servers are up. Input:1"
        print "Type 2: All servers are down. Input:2 "
        print "Type 3: Given a list of cells are down. Input:3 row1,col1 row2,col2 ..."
        print "Type 4: Let a rectangle region of cells down. Input:4 row1,col1 row2,col2"
        print "Type 5: All servers are up with a given probability. Input:5 probability"
        print "-----------------------------------------------------------------------"
                
    def start_controller(self):
        self.print_usage()
        while True:
            rawInput = raw_input("Please input control parameter:")
                
            paraList = rawInput.split(" ")
            ctype = paraList[0]
            change_region = set()
            
            if ctype == '1':
                print "Type " + ctype + ": All servers are up."
                self.fill_matrix(1)
                change_region = {x for x in range(num_region)}
                
            elif ctype == '2':
                print "type " + ctype + ": All servers are down."
                self.fill_matrix(0)
                change_region = {x for x in range(num_region)}
                
            elif ctype == '3':
                print "type " + ctype + ": the given list of cells are down."
                for i in range(len(paraList)):
                    if i != 0:
                        # the coordinate format is row,col
                        # if the format is (row,col), change r'\d+' to r'(\d+)'
                        row,col = map(int, re.findall(r'\d+', paraList[i]))
                        self.prob_matrix[row][col] = 0  
                        region_index = self.cell_to_region((row,col))
                        change_region.add(region_index)                            
                
            elif ctype == '4':
                print "type " + ctype + ": the rectangle region of cells are down."
                start_row, start_col = map(int, re.findall(r'\d+', paraList[1]))
                end_row, end_col = map(int, re.findall(r'\d+', paraList[2]))
                
                if start_row > end_row:
                    start_row, end_row = end_row, start_row # swap
                
                if start_col > end_col:
                    start_col, end_col = end_col, start_col # swap
                        
                self.fill_matrix(0, start_row, end_row+1, start_col, end_col+1)
                
                left_top_region = self.cell_to_region((start_row,start_col))
                right_down_region = self.cell_to_region((end_row,end_col))
                
                '''
                for i in range (start_row, end_row):
                    for j in range (start_col, end_col):
                        self.prob_matrix[i][j] = prob
                '''
                
                
                
            elif ctype == '5':
                prob = float(paraList[1])
                print "type " + ctype + ": All servers are up with " + str(prob*100) + "% probability."
                self.fill_matrix(prob) 
                change_region = {x for x in range(num_region)}
                  
            else:
                print "ERROR: Wrong control parameter!"
                continue
            self.print_matrix()
            self.assign_jobs(change_region)
            
    def initialize_worker_processes(self):
        pipe_pairs = [Pipe() for x in range(num_region)] #self.control_process
        self.process_workers = [Process(target = self.test_proc, args = (i, pipe_pairs[i][1])) for i in xrange(num_region)]
        self.pipes = [pipe_pair[0] for pipe_pair in pipe_pairs]
        map(lambda p:p.start(), self.process_workers)
        #for p in self.process_workers:
        #    p.start()

        # self.worker_pool = Pool(processes=num_region)
        # self.worker_pool.map_async(self.control_process, (x for x in xrange(num_region)))
        # pool.map_async(worker, (x for x in xrange(num_region)))
        # pool.close()
        # pool.join()
    
    def test_proc(self, index, pipe_conn):
        print "In test_proc:" + str(index)
        msg = pipe_conn.recv()
        print msg
    
        
    # Generate processes (#: num_region_x * num_region_y)
    # Each process generates threads (#: num_thread_region_x * num_thread_region_y)
    # to do the job (write 1/0 to files) 
    def assign_jobs(self, change_region):
        for i in change_region:
            self.pipes[i].send("Go!")
         
    def control_process(self, region_index, pipe_conn):
        print 'pid: %s, index: %s' % (os.getpid(), region_index)

        q = Queue.Queue()
    
        [threading.Thread(target = child_thread, args = (q, self.do_test_job)).start() for i in xrange(num_thread_region)]
        
        while True :
            msg = pipe_conn.recv() #wait for signal from pipe
            print "Worker process: " + str(region_index) + " "+ msg
            map(lambda thr_index : q.put(thr_index), thr_indice(region_index))
            q.join()
            print "Worker process: " + str(region_index) + " Done!"
    
    def do_test_job(self, cell):
        print cell
                            
    def do_control_job(self, cell):
        if cell == -1: #testing
            prob = self.prob_matrix[0][0]
            lines = []        
            with open("0-0", "r") as f:
                for aLine in f.readlines():
                    upOrDown = self.randUpOrDown(prob) 
                    aLine = aLine.split(" ") # split for only getting IP
                    #strip() to remove newline
                    newLine = aLine[0].strip() + " " + str(upOrDown) + "\n"
                    #print newLine
                    print repr(newLine)
                    lines.append(newLine)
                    #lines.append(aLine)
            with open("0-0", "w") as f:    
                f.writelines(lines)
        else: # x,y = cell
            row,col = cell
            prob = self.prob_matrix[row][col]
            lines = [] 
            filename = str(row)+"-"+str(col)       
            with open(filename, "r") as f:
                for aLine in f.readlines():
                    upOrDown = self.randUpOrDown(prob) 
                    aLine = aLine.split(" ") # split for only getting IP
                    #strip() to remove newline
                    newLine = aLine[0].strip() + " " + str(upOrDown) + "\n"
                    #print newLine
                    print repr(newLine)
                    lines.append(newLine)
                    #lines.append(aLine)
            with open(filename, "w") as f:    
                f.writelines(lines)
            
    # given probability, return 0 (server down) or 1 (server up)
    def randUpOrDown(self, prob):
        rand_num = random.random()
        if rand_num > prob:
            return 0
        else:
            return 1
    
    def print_matrix(self):
        for i in range (0, num_cell_y):
            for j in range (0, num_cell_x):
                print str(self.prob_matrix[i][j]) + "\t",
            print  


    

    