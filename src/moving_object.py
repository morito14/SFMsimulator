class MovingObject(object):
    """
    abstract class for robot, pedestrian
    """

    def __init__(self):
        # initialize
        self.position = [0., 0.]
        self.angle = 0.
        self.speed = 0.
        self.subgoal = [0., 0.]
        # social force
        self.f_wall = [0., 0.]
        self.f_pedestrian = [0., 0.]
        self.f_destination = [0., 0.]

    def get_status(self):
        # get status(angle, position, etc)
        return (self.position, self.angle, self.speed,
                self.subgoal)

    def set_status(self, **kwargs):
        # set status
        if 'position' in kwargs:
            self.position = kwargs['position']
        if 'angle' in kwargs:
            self.angle = kwargs['angle']
        if 'speed' in kwargs:
            self.speed = kwargs['speed']
        if 'subgoal' in kwargs:
            self.subgoal = kwargs['subgoal']


'''
    def calc_f_total(self, pedestrians, map, dt):
        # get total force

    def calc_f_wall(self, map, dt):
        # calc force from wall

    def calc_f_pedestrian(self, pedestrians, dt):
        # calc force from the other pedestrians
'''
