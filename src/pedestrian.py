from moving_object import MovingObject

class Pedestrian(MovingObject, object):
    '''robot, pedestrian'''

    def __init__(self):
        # initialize
        super(Pedestrian, self).__init__()
        self.radius = 0.3  # [m]
        self.color = [0, 0, 255]

'''
    def set_status(self):
        # set status

    def calc_f_total(self, pedestrians, map, dt):
        # get total force

    def calc_f_wall(self, map, dt):
        # calc force from wall

    def calc_f_pedestrian(self, pedestrians, dt):
        # calc force from the other pedestrians
'''
