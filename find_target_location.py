# Vincent Popie

import numpy as np
import scipy.optimize


class FindTarget:
    def __init__(self, sources_coord, time_differences):
        self.sources_coord = sources_coord
        self.time_differences = time_differences
        self.light_speed = 299792.458

    def objective_function(self, target_coord):
        res = 0.0
        for time_diff in self.time_differences:
            delta_t = time_diff["dt"]
            stations = time_diff["stations"]

            a = np.sqrt((target_coord[0] - self.sources_coord[stations[0]]['x']) ** 2 +
                        (target_coord[1] - self.sources_coord[stations[0]]['y']) ** 2)
            b = np.sqrt((target_coord[0] - self.sources_coord[stations[1]]['x']) ** 2 +
                        (target_coord[1] - self.sources_coord[stations[1]]['y']) ** 2)
            res += (delta_t*self.light_speed - (a - b)) ** 2
        return res

    def find_target_coord(self):
        target_coord = [0.0, 0.0]
        res = scipy.optimize.minimize(self.objective_function, target_coord,
                                      method='Nelder-Mead', tol=10e-8)
        return res.x
