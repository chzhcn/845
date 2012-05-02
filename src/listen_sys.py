import socket
import pickle
from defines import *

class lis():
    def __init__() :
        self.listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_sock.bind(report_addr)
        self.listening_sock.listen(5)

    def run(global_map) :
        while True :
            peer_socket, peer_address = listening_sock.accept()
            data = peer_socket.recv(8192 * 1024)
            peer_socket.close()
            map = pickle.loads(data);
            for k, v in map.iteritems():
                global_map[k] = v
            print map


if __name__ == '__main__' :
    
