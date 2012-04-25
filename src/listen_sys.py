import socket
import pickle
from defines import *

if __name__ == '__main__' :
    listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_sock.bind(report_addr)
    listening_sock.listen(5)

    while True :
        peer_socket, peer_address = listening_sock.accept()
        data = peer_socket.recv(8192 * 1024)
        peer_socket.close()
        map = pickle.loads(data);
        print map
