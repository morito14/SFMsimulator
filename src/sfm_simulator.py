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
        self.pedestrian = Pedestrian()

    def debug(self):
        # print('map={0}'.format(self.map.get_map()))
        self.pedestrian.set_status(speed=600, position=[10, 500])
        print('pedestrian status:{0}'.format(self.pedestrian.get_status()))
        print('map status:{0}'.format(self.map.get_status()))
        print('map.height:{0}, map.width:{1}'.format(self.map.height, self.map.width))

        while True:
            self.draw(self.pedestrian)
