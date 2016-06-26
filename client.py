# Vincent Popie

import sys
import socket
import json
import find_target_location


class Client:
    def __init__(self, host="localhost", port=1280):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.exe = True

    def connect(self):
        self.sock.connect((self.host, self.port))

    def receive(self):
        msg_received = self.sock.recv(1024)
        msg = msg_received.decode()
        stations_coord = json.loads(msg)
        try:
            while self.exe:
                msg_received = self.sock.recv(1024)
                msg = msg_received.decode()
                time_diff = json.loads(msg)

                find_target = find_target_location.FindTarget(stations_coord, time_diff)
                target_coord = find_target.find_target_coord()
                print('Target coordinates : x = {0}, y = {1}'.format(target_coord[0], target_coord[1]))

        except KeyboardInterrupt:  # Does not catch Ctrl-C because of scipy
            self.exe = False
            self.sock.close()
            print("Connection closed")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = str(sys.argv[1])
        my_client = Client(host)

    elif len(sys.argv) > 2:
        host = str(sys.argv[1])
        port = int(sys.argv[2])
        my_client = Client(host, port)

    else:
        my_client = Client()

    my_client.connect()
    my_client.receive()
