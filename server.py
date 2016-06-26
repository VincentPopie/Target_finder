# Vincent Popie

import sys
import socket
import select
import time
import data_generation


class Server:

    def __init__(self, port=1280, target_coord=(10, 10), nb_stations=4):
        self.host = ''
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_launch = False
        self.connected_client = []

        self.nb_stations = nb_stations
        self.target_coord = target_coord
        self.data = data_generation.GenerateData(self.nb_stations,
                                                 self.target_coord)

    def launch(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.server_launch = True

    def run(self):
        try:
            while self.server_launch:
                asked_connections, wlist, xlist = select.select([self.sock],
                                                                [], [], 0.05)

                for connection in asked_connections:
                    client_connection, info_connection = connection.accept()
                    self.connected_client.append(client_connection)

                    msg = self.data.convert_stations_coord()
                    client_connection.send(msg.encode())

                for client in self.connected_client:
                    msg = self.data.convert_time_diff()
                    try:
                        client.send(msg.encode())
                    except ConnectionResetError:
                        client.close()
                        self.connected_client.remove(client)
                time.sleep(1)
        except KeyboardInterrupt:
            self.server_launch = False

        print("Connection closed")
        self.sock.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        my_server = Server()
    elif len(sys.argv) < 4:
        port = int(sys.argv[1])
        my_server = Server(port)
    elif len(sys.argv) == 4:
        port = int(sys.argv[1])
        target_coord = [float(sys.argv[2]), float(sys.argv[3])]
        my_server = Server(port, target_coord)
    else:
        port = int(sys.argv[1])
        target_coord = [float(sys.argv[2]), float(sys.argv[3])]
        nb_stations = int(sys.argv[4])
        my_server = Server(port, target_coord, nb_stations)

    my_server.launch()
    my_server.run()
