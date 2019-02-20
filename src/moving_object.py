import numpy as np


class MovingObject(object):
    """
    abstract class for robot, pedestrian
    """

    def __init__(self):
        # initialize
        self.position = np.zeros(2)
        self.angle = 0.
        self.velocity = np.zeros(2)
        self.e_a = np.zeros(2)
        self.subgoal = np.zeros(2)
        self.color = [0, 0, 0]
        # social force (velocity vector)
        self.f_wall = np.zeros(2)
        self.closest_wall = np.zeros(2)
        self.f_pedestrian = np.zeros(2)
        self.f_destination = np.zeros(2)
        self.f_total = np.zeros(2)

    def get_status(self):
        # get status(angle, position, etc)
        return (self.position, self.angle, self.velocity,
                self.subgoal)

    def set_status(self, **kwargs):
        # set status
        if 'position' in kwargs:
            self.position = np.array(kwargs['position'])
        if 'angle' in kwargs:
            self.angle = kwargs['angle']
        if 'velocity' in kwargs:
            self.speed = kwargs['velocity']
        if 'subgoal' in kwargs:
            self.subgoal = kwargs['subgoal']
        if 'color' in kwargs:
            self.color = kwargs['color']

        print('set -> position:{0}, angle:{1}, velocity:{2}, subgoal{3}, color{4}'.format(
            self.position, self.angle, self.velocity, self.subgoal, self.color
        ))


