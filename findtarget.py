# Author : Vincent Popie

"""
Tool to find a target from propagation time difference between the target and
different sources

"""

import numpy as np
import scipy.optimize


class FindTarget:
    """
    Class defines to find a target

    """

    def __init__(self, sources_coord, time_differences):
        """

        :param sources_coord: list containing the sources coordinates
        :param time_differences: dict containing the time differences (dt)
        between two stations (stations)
        """
        self.sources_coord = sources_coord
        self.time_differences = time_differences
        self.light_speed = 299792.458

    def objective_function(self, target_coord):
        """
        Compute the objective function to minimize to find the target
        coordinates

        :param target_coord: coordinates of the target
        :return: the value of the objective function
        """
        res = 0.0
        for time_diff in self.time_differences:
            delta_t = time_diff["dt"]
            stations = time_diff["stations"]
            st0, st1 = stations

            a = np.sqrt((target_coord[0] - self.sources_coord[st0]['x']) ** 2 +
                        (target_coord[1] - self.sources_coord[st0]['y']) ** 2)
            b = np.sqrt((target_coord[0] - self.sources_coord[st1]['x']) ** 2 +
                        (target_coord[1] - self.sources_coord[st1]['y']) ** 2)
            res += (delta_t*self.light_speed - (a - b)) ** 2
        return res

    def find_target_coord(self):
        """
        Compute the target coordinates thanks to a Nelder-Mead minimization
        method

        :return: the target coordinates found
        """
        target_coord = [0.0, 0.0]
        res = scipy.optimize.minimize(self.objective_function, target_coord,
                                      method='Nelder-Mead', tol=10e-8)
        return res.x
