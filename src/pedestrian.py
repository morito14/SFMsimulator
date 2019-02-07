from moving_object import MovingObject

class Pedestrian(MovingObject, object):
    '''robot, pedestrian'''

    def __init__(self):
        # initialize
        super(Pedestrian, self).__init__()
        self.radius = 0.3  # [m]
        self.color = [0, 0, 255]
        self.desired_velocity = 1.08  # [m/s]

        print('generated pedestrian')

    def set_status(self, **kwargs):
        # set_status
        if 'desired_velocity' in kwargs:
            self.desired_velocity = kwargs['desired_velocity']

        print('set -> desired_velocity:{0}'.format(self.desired_velocity))
        super(Pedestrian, self).set_status(**kwargs)


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
