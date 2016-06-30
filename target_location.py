import sys
import json
import client
import find_target_location

if __name__ == '__main__':

    host = str(sys.argv[1])
    port = int(sys.argv[2])

    my_client = client.Client()
    my_client.connect(host, port)

    # Received first the station coords
    msg_received = my_client.receive()
    msg = msg_received.decode()
    stations_coord = json.loads(msg)

    try:
        while True:
            msg_received = my_client.receive()
            msg = msg_received.decode()
            time_diff = json.loads(msg)
            find_target = find_target_location.FindTarget(stations_coord, time_diff)
            target_coord = find_target.find_target_coord()
            print('Target coordinates : x = {0}, y = {1}'.format(target_coord[0], target_coord[1]))
    except KeyboardInterrupt:  # Does not catch Ctrl-C because of scipy
            my_client.close()
            print("Connection closed")
