# Vincent Popie

"""
Program which generates fictive data to use test target finder algorithms

"""
import argparse
import time

import server
import select

import generatedata

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="the socket port", type=int)
    parser.add_argument("x", help="the target x-coordinates", type=float)
    parser.add_argument("y", help="the target y-coordinates", type=float)
    parser.add_argument("nb_stations", help="the number of stations", type=int)
    args = parser.parse_args()

    target_coord = [args.x, args.y]

    my_server = server.Server()

    my_data = generatedata.GenerateData(args.nb_stations, target_coord)

    my_server.launch(args.port)

    try:
        while my_server.server_launch:
            asked_connections, wlist, xlist = \
                select.select([my_server.serversock], [], [], 0.05)
            for connection in asked_connections:
                client_connection, info_connection = connection.accept()
                my_server.connected_client.append(client_connection)

                msg = my_data.convert_stations_coord()
                my_server.mysend(msg.encode(), client_connection)

            for client in my_server.connected_client:
                msg = my_data.convert_time_diff()
                try:
                    my_server.mysend(msg.encode(), client)
                except ConnectionResetError:
                    client.close()
                    my_server.connected_client.remove(client)
            time.sleep(1)
    except KeyboardInterrupt:
        my_server.server_launch = False
        print("Connection closed")
        my_server.serversock.close()
