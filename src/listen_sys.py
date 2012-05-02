import socket
import pickle
from defines import *

class lis():
    def __init__(self) :
        self.listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_sock.bind(report_addr)
        self.listening_sock.listen(5)

    def run(self, global_map) :
        while True :
            peer_socket, peer_address = self.listening_sock.accept()
            data = peer_socket.recv(8192 * 1024)
            peer_socket.close()
            map = pickle.loads(data)[1];
            for k, v in map.iteritems():
                global_map[k] = v
            print map

if __name__ == '__main__' :
    pass

# <<<<<<< HEAD
# =======
#     listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     listening_sock.bind(report_addr)
#     listening_sock.listen(5)
#     count = 0
#     run = 0
#     while True :
#         peer_socket, peer_address = listening_sock.accept()
#         data = peer_socket.recv(8192 * 1024)
#         peer_socket.close()
#         msg = pickle.loads(data);
#         print 'process %s sends result map: %s' % (msg[0], msg[1])
#         if (0, 0) in msg[1].keys() and msg[1][(0, 0)] == 0 : 
#             count += 1
#         run += 1
#         if run >= num_collect :
#             break
#     print 'count = %s, run = %s, rate = %s' % (count, run, float(count/run))
# >>>>>>> origin/master
