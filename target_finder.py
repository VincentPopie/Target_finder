# author : Vincent Popie

"""
Main program to find target coordinates from the propagation time difference
between the target and different sources.


"""

import argparse
import json

import client
import findtarget

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="the server host")
    parser.add_argument("port", help="the server port", type=int)
    args = parser.parse_args()

    my_client = client.Client()
    my_client.connect(args.host, args.port)

    # Received first the station coords
    msg_received = my_client.myreceive()
    msg = msg_received.decode()
    stations_coord = json.loads(msg)

    try:
        while True:
            msg_received = my_client.myreceive()
            msg = msg_received.decode()
            time_diff = json.loads(msg)
            find_target = findtarget.FindTarget(stations_coord, time_diff)
            target_coord = find_target.find_target_coord()
            print('Target coordinates : x = {0}, y = {1}'
                  .format(target_coord[0], target_coord[1]), flush=True)
    except KeyboardInterrupt:  # Does not catch Ctrl-C because of scipy
            my_client.close()
            print("Connection closed")
