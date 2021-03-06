# author : Vincent Popie
# Warning : created for Python3.x (division between 2 ints)

"""
Generate fictive data to test the algorithm to find target coordinates

"""

import math
import json


class Station:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def build_json(self):
        return self.__dict__


class TimeDifference:
    def __init__(self, stations, dt):
        self.stations = stations
        self.dt = dt

    def build_json(self):
        return self.__dict__


class GenerateData:
    def __init__(self, nb_stations, target_coord):
        """
        Generate fictive data to test the algorithm to find target coordinates

        :param nb_stations: number of stations
        :param target_coord: coordinates of the target
        """
        self.light_speed = 299792.458

        self.nb_stations = nb_stations
        self.target_coord = Station(target_coord[0], target_coord[1])

        self.stations_coord = []
        self.compute_stations_coord()

        self.propagation_time = []
        self.compute_propagation_time()

        self.time_diff = []
        self.compute_time_diff()

    def compute_stations_coord(self):
        """
        Compute the coordinates of the different stations
        The stations are distributed on the unit circle

        :return: a list with the stations coordinates
        """
        for i in range(0, self.nb_stations):
            theta = i / self.nb_stations
            x = math.cos(2 * math.pi * theta)
            y = math.sin(2 * math.pi * theta)
            self.stations_coord.append(Station(x, y))

    def compute_propagation_time(self):
        """
        :return: the propagation time between the target and a station
        """
        for stations in self.stations_coord:
            d = math.sqrt((stations.x - self.target_coord.x) ** 2 +
                          (stations.y - self.target_coord.y) ** 2)
            t = d / self.light_speed
            self.propagation_time.append(t)

    def compute_time_diff(self):
        """
        Compute the propagation time difference between the target and each
        station

        :return: a list of TimeDifference
        """
        for i in range(0, self.nb_stations):
            for j in range(i + 1, self.nb_stations):
                diff = self.propagation_time[i] - self.propagation_time[j]
                if diff < 0:
                    self.time_diff.append(TimeDifference([j, i], -diff))
                else:
                    self.time_diff.append(TimeDifference([i, j], diff))

    def convert_stations_coord(self):
        return json.dumps(self.stations_coord, default=Station.build_json)

    def convert_time_diff(self):
        return json.dumps(self.time_diff, default=TimeDifference.build_json)
