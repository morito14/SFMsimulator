from moving_object import MovingObject
import numpy as np


class Pedestrian(MovingObject, object):
    '''robot, pedestrian'''

    def __init__(self):
        # initialize
        super(Pedestrian, self).__init__()
        self.radius = 0.3  # [m]
        self.color = [0, 0, 255]
        self.desired_velocity = 1.08  # [m/s]
        self.tau = 0.1  # relaxation time

        print('generated pedestrian')

    def set_status(self, **kwargs):
        # set_status
        if 'desired_velocity' in kwargs:
            self.desired_velocity = kwargs['desired_velocity']

        print('set -> desired_velocity:{0}'.format(self.desired_velocity))
        super(Pedestrian, self).set_status(**kwargs)

    def calc_f_total(self, pedestrians, slam_map, dt):
        # get total force
        self.f_wall = self.calc_f_wall(slam_map, dt)
        self.f_pedestrian = self.calc_f_pedestrian(pedestrians, dt)
        self.calc_f_destination()

        return self.f_wall + self.f_pedestrian + self.f_destination

    def calc_f_wall(self, map, dt):
        # calc force from wall
        print('todo')
        return [0, 0]

    def calc_f_pedestrian(self, pedestrians, dt):
        # calc force from the other pedestrians
        print('todo')
        return [0, 0]

    def calc_f_destination(self):
        # calc force from destination
        # unit vector for desired direction
        e_a = (self.subgoal - self.position) / np.linalg.norm(self.subgoal - self.position)
        f_destination = (self.desired_velocity * e_a - self.velocity) / self.tau
        # print('desired_vel:{0}, e_a:{1}'.format(self.desired_velocity, e_a))
        print('f_destination:{0}'.format(f_destination))

        self.f_destination = f_destination
        return f_destination
