from disaster_controller import *
  
 #print dc.normal_prob
    #print dc.print_matrix()
    #dc.control_thread(-1)       
if __name__ == '__main__' :
    dc = disaster_controller() 
   
    dc.start_controller()
    
    #cell = (6,14)
    #print dc.cell_to_region(cell)
    