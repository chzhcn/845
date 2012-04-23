from defines import *
import os # os.linesep
import random
import re
import threading
import thread
from multiprocessing import Pool, Process, Pipe
from thr import child_thread
from util import thr_indice

'''
self.thread_stream = threading.Thread(target=self.stream_music, args=(message,))
339 self.thread_stream.start()
def stream_music(self, message) :
'''

class disaster_controller:
    #broken_prob = 0.8
    fail_threshold = 0.6
    normal_prob = 0.95
    # size of matrix is the same as the map
    # each element's value is the probability of disaster NOT happening
    prob_matrix = None 
    rand_seed = 0
    rand_amount = 100 # used to control accuracy
    def __init__(self):
        self.rand_seed = random.randint(0,100000)
        self.prob_matrix = []
        for i in range (0, num_cell_y):
            aRow = []
            for j in range (0, num_cell_x):
                aRow.append(self.normal_prob)
            self.prob_matrix.append(aRow)  
    
    def fill_matrix(self, prob, start_row = 0, end_row = num_cell_y, start_col = 0, end_col = num_cell_x):
        # check boundary
        if start_row < 0 or end_row > num_cell_y or start_col < 0 or end_col > num_cell_x:
            print "ERROR: Given boundary is wrong!"
            print "row range: (0, " + str(num_cell_y-1) + ") column range: (0, " + str(num_cell_x-1) + ")"
            return  
        
        for i in range (start_row, end_row):
            for j in range (start_col, end_col):
                self.prob_matrix[i][j] = prob
    
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
            
            if ctype == '1':
                print "Type " + ctype + ": All servers are up."
                self.fill_matrix(1)
                self.print_matrix()
                
            elif ctype == '2':
                print "type " + ctype + ": All servers are down."
                self.fill_matrix(0)
                self.print_matrix()
                
            elif ctype == '3':
                print "type " + ctype + ": the given list of cells are down."
                for i in range(len(paraList)):
                    if i != 0:
                        # the coordinate format is row,col
                        # if the format is (row,col), change r'\d+' to r'(\d+)'
                        row,col = map(int, re.findall(r'\d+', paraList[i]))
                        self.prob_matrix[row][col] = 0                        
                self.print_matrix()        
                
            elif ctype == '4':
                print "type " + ctype + ": the rectangle region of cells are down."
                start_row, start_col = map(int, re.findall(r'\d+', paraList[1]))
                end_row, end_col = map(int, re.findall(r'\d+', paraList[2]))
                
                if start_row > end_row:
                    start_row, end_row = end_row, start_row # swap
                
                if start_col > end_col:
                    start_col, end_col = end_col, start_col # swap
                        
                self.fill_matrix(0, start_row, end_row+1, start_col, end_col+1)
                self.print_matrix()
            
            elif ctype == '5':
                prob = float(paraList[1])
                print "type " + ctype + ": All servers are up with " + str(prob*100) + "% probability."
                self.fill_matrix(prob)
                self.print_matrix()    
            else:
                print "ERROR: Wrong control parameter!"
    
    # Generate processes (#: num_region_x * num_region_y)
    # Each process generates threads (#: num_thread_region_x * num_thread_region_y)
    # to do the job (write 1/0 to files) 
    def assign_jobs(self):
        p = Process(target = self.control_process, args=(31,))
        p.start()
        p.join()
    
    def control_process(self, region_index):
        print 'pid: %s, index: %s' % (os.getpid(), region_index)

        q = Queue.Queue()
    
        [threading.Thread(target = child_thread, args = (q, self.do_control_job)).start() for i in xrange(num_thread_region)]
    
        while True :
            map(lambda thr_index : q.put(thr_index), thr_indice(region_index))
            q.join()
            print 'one iteration'
                        
    def do_control_job(self, region_code):
        if region_code == -1: #testing
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
          
    # given probability, return 0 (server down) or 1 (server up)
    def randUpOrDown(self, prob):
        random.seed(self.rand_seed)
        self.rand_seed = self.rand_seed+1
        upList = [1]*(int(prob*self.rand_amount))
        downList = [0]*(int((1-prob)*self.rand_amount))
        comList = upList + downList
        #random.shuffle(comList)
        #Return a random element from the non-empty sequence seq. If seq is empty, raises IndexError.
        return random.choice(comList)
    
    def print_matrix(self):
        for i in range (0, num_cell_y):
            for j in range (0, num_cell_x):
                print str(self.prob_matrix[i][j]) + "\t",
            print  



    