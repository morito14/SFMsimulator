# coding=utf-8
from map import Map
from drawer import Drawer
from pedestrian import Pedestrian
from robot import Robot
import numpy as np
import time


class SFMSimulator(Drawer, object):
    """
    Social Force Model simulator

    """

    def __init__(self, path_to_map, path_to_yaml, **kwargs):
        # initialize drawer
        self.slam_map = Map(path_to_map, path_to_yaml)
        zoom = kwargs['zoom'] if 'zoom' in kwargs else 1
        super(SFMSimulator, self).__init__(self.slam_map, zoom)
        self.dt = kwargs['dt'] if 'dt' in kwargs else 0.01 # time-step [sec]
        # initialize pedestrian
        self.pedestrians = []
        self.robots = []

    def debug(self):
        self.generate_pedestrian(position=[-2, 2], subgoal=[-2, 0])
        self.generate_pedestrian(position=[-2, -2], subgoal=[-2, 0])
        self.generate_pedestrian(position=[1.1, -2], subgoal=[-2, 0])
        self.generate_pedestrian(position=[1.1, 2], subgoal=[-2, 0])

        while True:
            start = time.time()
            for pedestrian in self.pedestrians:
                pedestrian.calc_f_total(self.pedestrians, self.slam_map)
                pedestrian.update_velocity(self.dt)
                pedestrian.update_position(self.dt)

            self.draw(self.pedestrians, self.robots)
            process_time = time.time() - start
            print('time(1-loop):{0}'.format(process_time))
            time.sleep(self.dt)
            # if np.linalg.norm(self.pedestrians[0].subgoal - self.pedestrians[0].position) < 0.1:
            #     break

    def generate_pedestrian(self, **kwargs):
        self.pedestrians.append(Pedestrian())
        self.pedestrians[-1].set_status(**kwargs)

    def generate_robot(self, **kwargs):
        self.robots.append(Robot())
        self.robots[-1].set_status(**kwargs)
