# coding=utf-8
from map import Map
from drawer import Drawer
from pedestrian import Pedestrian
from robot import Robot


class SFMSimulator(Drawer, object):
    """
    Social Force Model simulator

    """

    def __init__(self, path_to_map, path_to_yaml, **kwargs):
        # initialize drawer
        self.slam_map = Map(path_to_map, path_to_yaml)
        zoom = kwargs['zoom'] if 'zoom' in kwargs else 1
        super(SFMSimulator, self).__init__(self.slam_map, zoom)
        # initialize pedestrian
        self.pedestrians = []
        self.robots = []

    def debug(self):
        self.generate_pedestrian(position=[0, 0], subgoal=[1, 0])
        self.generate_pedestrian(position=[1, 0], subgoal=[1, 0])
        self.generate_pedestrian(position=[15, 0], subgoal=[1, 0])
        self.generate_pedestrian(position=[1, 1], subgoal=[1, 0])
        self.pedestrians[0].calc_f_destination()
        self.pedestrians[0].calc_f_pedestrian(self.pedestrians)
        # print(self.pedestrians[0].f_wall)
        # self.generate_robot()

        while True:
            self.draw(self.pedestrians, self.robots)

    def generate_pedestrian(self, **kwargs):
        self.pedestrians.append(Pedestrian())
        self.pedestrians[-1].set_status(**kwargs)

    def generate_robot(self, **kwargs):
        self.robots.append(Robot())
        self.robots[-1].set_status(**kwargs)
