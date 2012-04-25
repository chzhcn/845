import sys
import os
import socket
from defines import *

IP_BASE = 3221225472            # 192.0.0.0

def inttoip(ip):
    return socket.inet_ntoa(hex(ip)[2:].zfill(8).decode('hex'))

def IntToDottedIP( intip ):
    octet = ''
    for exp in [3,2,1,0]:
            octet = octet + str(intip / ( 256 ** exp )) + "."
            intip = intip % ( 256 ** exp )
    return(octet.rstrip('.'))
    
if __name__ == '__main__' :
    data_dir = sys.argv[1]
    ip_inc = 0

    x, y = 0, 0
    
    for x in xrange(num_cell_x) :
        for y in xrange(num_cell_y) :           #             #
            cell_path = data_dir + os.sep +  str(y) + '-' + str(x) # generate the file name
            with open(cell_path, 'w') as cell_file :
            # cell_file = open(cell_path, 'w')
                lines = []
                for i in xrange(server_per_cell) : # generate fake IPs
                    ip_inc += 1
                    aLine = IntToDottedIP(ip_inc + IP_BASE) + ' 1' + os.linesep
                    lines.append(aLine)
                    #print repr(aLine)
                cell_file.writelines(lines)
            # cell_file.close()


