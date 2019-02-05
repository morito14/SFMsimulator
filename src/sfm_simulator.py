# coding=utf-8
from map import Map
from drawer import Drawer
from pedestrian import Pedestrian


class SFMSimulator(Drawer, object):
    """
    Social Force Model simulator

    """

    def __init__(self, path_to_map, path_to_yaml, **kwargs):
        # initialize drawer
        self.map = Map(path_to_map, path_to_yaml)
        zoom = kwargs['zoom'] if 'zoom' in kwargs else 1
        super(SFMSimulator, self).__init__(self.map, zoom)
        # initialize pedestrian
        self.pedestrians = []

    def debug(self):
        for num in range(10):
            self.generate_pedestrian(speed=num)
        for pedestrian in self.pedestrians:
            print(pedestrian.speed)

        while True:
            self.draw(self.pedestrians)

    def generate_pedestrian(self, **kwargs):
        self.pedestrians.append(Pedestrian())
        self.pedestrians[-1].set_status(**kwargs)
