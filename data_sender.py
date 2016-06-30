import sys
import server
import select
import time
import generatedata

if __name__ == '__main__':
    port = int(sys.argv[1])
    target_coord = [float(sys.argv[2]), float(sys.argv[3])]
    nb_stations = int(sys.argv[4])

    my_server = server.Server()

    my_data = generatedata.GenerateData(nb_stations, target_coord)

    my_server.launch(port)

    try:
        while my_server.server_launch:
            asked_connections, wlist, xlist = select.select([my_server.serversock],
                                                            [], [], 0.05)
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

