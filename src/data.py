import sys
import os
import socket
from defines import *

IP_BASE = 3221225472            # 192.0.0.0

def inttoip(ip):
    return socket.inet_ntoa(hex(ip)[2:].zfill(8).decode('hex'))

if __name__ == '__main__' :
    data_dir = sys.argv[1]
    ip_inc = 0

    x, y = 0, 0
    
    for x in range(num_cell_x) :
        for y in range(num_cell_y) :
            cell_path = data_dir + os.sep +  str(x) + '-' + str(y) # generate the file name
            with open(cell_path, 'w') as cell_file :
            # cell_file = open(cell_path, 'w')
                lines = []
                for i in range(server_per_cell) : # generate fake IPs
                    ip_inc += 1
                    lines.append(inttoip(ip_inc + IP_BASE) + os.linesep)
                cell_file.writelines(lines)
            # cell_file.close()


